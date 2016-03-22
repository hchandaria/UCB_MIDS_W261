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
#@epsilon = smoothing
# return partially calculated  rnk (numerator)
def bernoulli(terms, alpha,qmk_local,epsilon):
    lprob = 0.0 #log probability
    for i in range(len(qmk_local)):
        if np.isnan(terms[i]) : #if we have never seen the term in the document 
            continue
        lprob += log(terms[i]*(qmk_local[i] + epsilon) + ((1-terms[i] )*(1-qmk_local[i] + epsilon)))
    lprob =  Decimal(log(alpha)+lprob).exp()
    return lprob
        
        

class MrBMixEm(MRJob):
    DEFAULT_PROTOCOL = 'json'
    
    def __init__(self, *args, **kwargs):
        super(MrBMixEm, self).__init__(*args, **kwargs)
        
        fullPath = self.options.pathName + 'intermediateResults_BMM_tweet.txt'
        fileIn = open(fullPath)
        inputJson = fileIn.read()
        fileIn.close()
        inputList = json.loads(inputJson)
        temp = inputList[0]        
        self.alpha = array(temp)           #prior class probabilities
        self.qmk = inputList[1] #entire vocab   
        self.vocab = [] # for the first round determing which indexes have data
        self.new_qmk = zeros_like(self.qmk)
        for i in range(len(self.qmk)) :
            for j in range(len(self.qmk[i])):
                if(self.qmk[i][j] != 0):
                    self.vocab.append(j)
                
        self.vocab =  set(self.vocab)
            
        self.new_alphas = zeros_like(self.alpha)        #partial weighted sum of weights
        
#         self.numMappers = 1             #number of mappers
        self.count = 0                  #passes through mapper

        
    def configure_options(self):
        super(MrBMixEm, self).configure_options()

        self.add_passthrough_option(
            '--k', dest='k', default=4, type='int',
            help='k: number of densities in mixture')
        self.add_passthrough_option(
            '--pathName', dest='pathName', default="", type='str',
            help='pathName: pathname where intermediateResults.txt is stored')
        
    def mapper(self, key, line):
        smoothing = 0.0001
        #accumulate partial sums for each mapper
        val = line.strip().split(',')[3:]
        stripe=zeros([len(val)])
        
        for i in range(len(val)):
            if i not in self.vocab:
                continue
            if val[i] != '0' :
                stripe[i] = 1.0
            else : stripe[i]= None
    
        rnk=zeros_like(self.alpha)
        
        for i in range(0,self.options.k):
            rnk[i] = bernoulli(stripe,self.alpha[i],self.qmk[i],smoothing)
    
        rnk = rnk/sum(rnk)
   
        #increment counts 
        self.count += 1
        
        #accumulate new alpha 
        self.new_alphas = self.new_alphas + (rnk)# + smoothing)
        
        for i in range(self.options.k):
            for j in range(len(val)):
                if val[j] == '0':
                    continue
                self.new_qmk[i][j] +=  (rnk[i])# + smoothing)
#         dummy yield - real output passes to mapper_final in self

        
    def mapper_final(self):
        
        out = [self.count, (self.new_alphas).tolist(),self.new_qmk.tolist() ]
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
                totqmk = array(temp[2])         
                first = False
            else:
                temp = json.loads(val)
                #cumulative sum of four arrays
                totCount = totCount + temp[0]
                totalpha = totalpha + array(temp[1])
                totqmk  = totqmk + array(temp[2])
                
        #finish calculation of new probability parameters. array divided by array
        newAlpha = totalpha/totCount
#         print array(newAlpha).tolist()
        #initialize these to something handy to get the right size arrays
        newqmk = zeros_like(totqmk)
        for i in range(self.options.k):
            for j in range(len(totqmk[i])):
                newqmk[i][j] = totqmk[i][j]/totalpha[i]
            
        outputList = [newAlpha.tolist(),newqmk.tolist()]
        jsonOut = json.dumps(outputList)
        
        #write new parameters to file
        fullPath = self.options.pathName + 'intermediateResults_BMM_tweet.txt'
        fileOut = open(fullPath,'w')
        fileOut.write(jsonOut)
        fileOut.close()

if __name__ == '__main__':
    MrBMixEm.run()