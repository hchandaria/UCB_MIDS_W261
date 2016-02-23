from __future__ import division
from mrjob.job import MRJob

from math import sqrt, exp, pow,pi
from numpy import zeros, shape, random, array, zeros_like, dot, linalg
import json, re

WORD_RE = re.compile(r"[\w']+")

# @terms = terms present in the incoming document
# @alpha = prior probability for cluster k
# @qmk_local = vocab probability for cluster k
# return partially calculated  rnk (numerator)
def bernoulli(terms, alpha,qmk_local,n,k):
    rnk_present = 0.0
    rnk_absent = 0.0
    rnk_local= 0.0
#     print terms
#     print qmk_local
    for key,value in qmk_local.iteritems():
        if key in terms:
#             print "value",value
            rnk_present += value
        else:
            rnk_absent += (1.0-value)
#     print "N,K,present,absent: ",n,k,rnk_present,rnk_absent
    rnk_local = alpha*(rnk_present*rnk_absent)
    return rnk_local
        
        

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
        
        self.new_qmk = {}
        for i in range(self.options.k):
            self.new_qmk[i]={}
        for key,value in self.qmk.iteritems():
            for term,val in value.iteritems():
                self.new_qmk[key][term]=0
        
        
        self.new_alphas = zeros_like(self.alpha)        #partial weighted sum of weights
        
        self.numMappers = 1             #number of mappers
        self.count = 0                  #passes through mapper
        
        print 'from init:',self.qmk
        
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
        stripe ={} 
        for word in val:
            if word in stripe:
                continue
            stripe[word]=1
        rnk=zeros_like(self.alpha)
        print 'Mapper',self.count,self.qmk
        for i in range(0,self.options.k):
            rnk[i] = bernoulli(stripe,self.alpha[i],self.qmk[i],self.count,i)
        rnkSum = sum(rnk)
        if(rnkSum ==0):
            rnk=zeros_like(self.alpha)
        else:
            rnk = rnk/rnkSum
        yield self.count, rnk.tolist()
        #increment counts 
        self.count += 1
        
#         #accumulate new alpha 
#         self.new_alphas = self.new_alphas + (rnk + smoothing)
        
#         for i in range(self.options.k):
#             for key,value in self.new_qmk[i].iteritems():
#                 if key not in stripe:
#                     continue
#                 self.new_qmk[i][key] = value + (rnk[i] + smoothing)
        #dummy yield - real output passes to mapper_final in self

        
#     def mapper_final(self):
        
#         out = [self.count, (self.new_alphas).tolist(),self.new_qmk ]
#         jOut = json.dumps(out)        
        
#         yield 1,jOut
    
    
#     def reducer(self, key, xs):
#         #accumulate partial sums
#         first = True        
#         #accumulate partial sums
#         #xs us a list of paritial stats, including count, phi, mean, and covariance. 
#         #Each stats is k-length array, storing info for k components
#         for val in xs:
#             if first:
#                 temp = json.loads(val)
#                 #totCount, totPhi, totMeans, and totCov are all arrays
#                 totCount = temp[0]
#                 totalpha = array(temp[1])
#                 totqmk = {int(k):v for k,v in temp[2].items()}            
#                 first = False
#             else:
#                 temp = json.loads(val)
#                 #cumulative sum of four arrays
#                 totCount = totCount + temp[0]
#                 totalpha = totalpha + array(temp[1])
#                 local_qmk = {int(k):v for k,v in temp[2].items()}
#                 for key,value in totqmk.iteritems():
#                     for term,count in value.iteritems():
#                         totqmk[key][term] = count + local_qmk[key][term]
                
#         #finish calculation of new probability parameters. array divided by array
#         newAlpha = totalpha/totCount
#         #initialize these to something handy to get the right size arrays
#         newqmk = {}
#         for i in range(self.options.k):
#             newqmk[i]={}
#             for key,value in totqmk[i].iteritems():
#                 newqmk[i][key] = value/totalpha[i]
            
#         print newqmk
#         yield newAlpha, newqmk
#         outputList = [newAlpha.tolist(),newqmk]
#         jsonOut = json.dumps(outputList)
        
#         #write new parameters to file
#         fullPath = self.options.pathName + 'intermediateResults_BMM.txt'
#         fileOut = open(fullPath,'w')
#         fileOut.write(jsonOut)
#         fileOut.close()

if __name__ == '__main__':
    MrBMixEm.run()