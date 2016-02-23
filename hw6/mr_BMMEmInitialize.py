from __future__ import division
from mrjob.job import MRJob

from numpy import mat, zeros, shape, random, array, zeros_like, dot, linalg
from random import sample
import json, re
from math import pi, sqrt, exp, pow

WORD_RE = re.compile(r"[\w']+")

class MrBMM_EmInit(MRJob):
#     DEFAULT_PROTOCOL = 'json'
    vocab={}
    qmk ={}
    
    def __init__(self, *args, **kwargs):
        super(MrBMM_EmInit, self).__init__(*args, **kwargs)
        
        self.numMappers = 1     #number of mappers
        self.count = 0
        
        
                                                 
    def configure_options(self):
        super(MrBMM_EmInit, self).configure_options()
        self.add_passthrough_option(
            '--k', dest='k', default=2, type='int',
            help='k: number of densities in mixture')
        self.add_passthrough_option(
            '--pathName', dest='pathName', default="", type='str',
            help='pathName: pathname where intermediateResults_BMM.txt is stored')
    
    def mapper_init(self):
        for i in range (0,self.options.k):
            self.vocab[i]={}
        #build vocab first
        with open('BMMtest.txt') as f:
            for line in f:
                words = re.findall(WORD_RE,line)
                for word in words:
                    for i in range(self.options.k):
                        if word in self.vocab[i]:
                            continue
                        self.vocab[i][word]=0
    
    def mapper(self, key, xjIn):
        #something simple to grab random starting point
        #collect the first 2k
        self.count += 1
        if self.count == 6:         
            yield (0,xjIn) 
        if self.count ==7:
            yield(1,xjIn)
        
    def reducer(self, key, xjIn):
        for xj in xjIn:
            words = re.findall(WORD_RE,xj)
            for word in words:
                if word not in self.vocab[key]:
                    continue
                self.vocab[key][word]=1
                yield key, word
                
        jDebug = json.dumps([self.vocab])    
        debugPath = self.options.pathName + 'debug_BMM.txt'
        fileOut = open(debugPath,'w')
        fileOut.write(jDebug)
        fileOut.close()
        
        #also need a starting guess at the phi's - prior probabilities
        #initialize them all with the same number - 1/k - equally probably for each cluster
        
        alpha = zeros(self.options.k,dtype=float)
        
        for i in range(self.options.k):
            alpha[i] = 1.0/float(self.options.k)
        
        #form output object
        outputList = [alpha.tolist(),self.vocab]
            
        jsonOut  = json.dumps(outputList)
        
        #write new parameters to file
        fullPath = self.options.pathName + 'intermediateResults_BMM.txt'
        fileOut = open(fullPath,'w')
        fileOut.write(jsonOut)
        fileOut.close()
        

if __name__ == '__main__':
    MrBMM_EmInit.run()