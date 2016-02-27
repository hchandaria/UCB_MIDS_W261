from __future__ import division
from mrjob.job import MRJob

from math import sqrt, exp, pow,pi
from numpy import zeros, shape, random, array, zeros_like, dot, linalg, log,exp
import numpy as np
import json, re
import collections
from decimal import *

WORD_RE = re.compile(r"[\w']+")

# @terms = terms present in the incoming document
# @alpha = prior probability for cluster k
# @qmk_local = vocab probability for cluster k
# return partially calculated  rnk (numerator)
def bernoulli(terms, alpha,qmk_local,n,k,epsilon):
    lprob = 0.0 #log probability
    for key,value in qmk_local.iteritems():
        if key not in terms: #if we have never seen the term in the document 
            continue
        lprob += log(terms[key]*(value + epsilon) + ((1-terms[key] )*(1-value + epsilon)))
    lprob =  Decimal(log(alpha)+lprob).exp()
    return lprob
        
        

class MrBMixEm(MRJob):
    DEFAULT_PROTOCOL = 'json'
    
    def __init__(self, *args, **kwargs):
        super(MrBMixEm, self).__init__(*args, **kwargs)
        
        fullPath = self.options.pathName + 'intermediateResults_BMM.txt'
        fileIn = open(fullPath)
        inputJson = fileIn.read()
        fileIn.close()
        inputList = json.loads(inputJson)
        temp = inputList[0]        
        self.alpha = array(temp)           #prior class probabilities
        temp = inputList[1] #entire vocab         
        
        self.qmk = {int(k):v for k,v in temp.items()}
        
        self.vocab = []
        self.new_qmk = {}
        for i in range(self.options.k):
            self.new_qmk[i]={}
        for key,value in self.qmk.iteritems():
            for term,val in value.iteritems():
                self.new_qmk[key][term]=0
                if(val != 0):
                    self.vocab.append(term)
                
        self.vocab =  set(self.vocab)
            
        self.new_alphas = zeros_like(self.alpha)        #partial weighted sum of weights
        
        self.numMappers = 1             #number of mappers
        self.count = 0                  #passes through mapper

        
    def configure_options(self):
        super(MrBMixEm, self).configure_options()

        self.add_passthrough_option(
            '--k', dest='k', default=2, type='int',
            help='k: number of densities in mixture')
        self.add_passthrough_option(
            '--pathName', dest='pathName', default="", type='str',
            help='pathName: pathname where intermediateResults.txt is stored')
        
    def mapper(self, key, val):
        smoothing = 0.0001
        #accumulate partial sums for each mapper
        val = re.findall(WORD_RE,val)
        stripe ={k: 0 for k in self.vocab} 
        
    
        for word in val:
            if word not in stripe:
                continue
            stripe[word]=1
        rnk=zeros_like(self.alpha)
        
        for i in range(0,self.options.k):
            rnk[i] = bernoulli(stripe,self.alpha[i],self.qmk[i],self.count,i,smoothing)

        rnk = rnk/sum(rnk)
   
        #increment counts 
        self.count += 1
        
        #accumulate new alpha 
        self.new_alphas = self.new_alphas + (rnk + smoothing)
        
        
        print "Doc Probability: ",self.count,[round(i,4) for i in rnk]
        
        for i in range(self.options.k):
            for key in val:
                self.new_qmk[i][key] +=  (rnk[i] + smoothing)
#         dummy yield - real output passes to mapper_final in self

        
    def mapper_final(self):
        
        out = [self.count, (self.new_alphas).tolist(),self.new_qmk ]
        jOut = json.dumps(out)
        yield 1,jOut
    
    
    def reducer(self, key, xs):
        #accumulate partial sums
        first = True        
        #accumulate partial sums
        #xs us a list of paritial stats, including count, phi, mean, and covariance. 
        #Each stats is k-length array, storing info for k components
        for val in xs:
            if first:
                temp = json.loads(val)
                #totCount, totPhi, totMeans, and totCov are all arrays
                totCount = temp[0]
                totalpha = array(temp[1])
                totqmk = {int(k):v for k,v in temp[2].items()}            
                first = False
            else:
                temp = json.loads(val)
                #cumulative sum of four arrays
                totCount = totCount + temp[0]
                totalpha = totalpha + array(temp[1])
                local_qmk = {int(k):v for k,v in temp[2].items()}
                for key,value in totqmk.iteritems():
                    for term,count in value.iteritems():
                        totqmk[key][term] = count + local_qmk[key][term]
                
        #finish calculation of new probability parameters. array divided by array
        newAlpha = totalpha/totCount
        print array(newAlpha).tolist()
        #initialize these to something handy to get the right size arrays
        newqmk = {}
        for i in range(self.options.k):
            newqmk[i]={}
            for key,value in totqmk[i].iteritems():
                newqmk[i][key] = value/totalpha[i]
            
        outputList = [newAlpha.tolist(),newqmk]
        jsonOut = json.dumps(outputList)
        
        #write new parameters to file
        fullPath = self.options.pathName + 'intermediateResults_BMM.txt'
        fileOut = open(fullPath,'w')
        fileOut.write(jsonOut)
        fileOut.close()

if __name__ == '__main__':
    MrBMixEm.run()