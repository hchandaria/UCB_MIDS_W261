from __future__ import division
from mrjob.job import MRJob

import numpy as np
from random import sample
import json, re
from math import pi, sqrt, exp, pow

WORD_RE = re.compile(r"[\w']+")

class MrBMM_EmInit(MRJob):
#     DEFAULT_PROTOCOL = 'json
    
    def __init__(self, *args, **kwargs):
        super(MrBMM_EmInit, self).__init__(*args, **kwargs)
        
        self.numMappers = 1     #number of mappers
        self.count = 0
        
                                                 
    def configure_options(self):
        super(MrBMM_EmInit, self).configure_options()
        self.add_passthrough_option(
            '--k', dest='k', default=4, type='int',
            help='k: number of densities in mixture')
        self.add_passthrough_option(
            '--pathName', dest='pathName', default="", type='str',
            help='pathName: pathname where intermediateResults_BMM.txt is stored')  
    
    def mapper(self, key, xjIn):
        if self.count <= 2*self.options.k:
            self.count += 1
            yield (1,xjIn) 

    def reducer(self, key, xjIn):
        cent=[]
        for xj in xjIn:
            terms = xj.strip().split(',')[3:]
            cent.append(terms) #append the data points 
        index = sample(range(len(cent)), self.options.k) #based on the number of clusters, select those many points randomly
        
        qmk =np.zeros([self.options.k,len(cent[0])])
        qmk_i = 0
        for i in index:
            for j in range(len(cent[i])):
                if (cent[i][j] == '0' ):
                    continue
                qmk[qmk_i][j]=1
            qmk_i +=1
               
        #also need a starting guess at the phi's - prior probabilities
        #initialize them all with the same number - 1/k - equally probably for each cluster
        
        alpha = np.zeros(self.options.k,dtype=float)
        
        for i in range(self.options.k):
            alpha[i] = 1.0/float(self.options.k)
        
        #form output object
        outputList = [alpha.tolist(),qmk.tolist()]
            
        jsonOut  = json.dumps(outputList)
        
        #write new parameters to file
        fullPath = self.options.pathName + 'intermediateResults_BMM_tweet.txt'
        fileOut = open(fullPath,'w')
        fileOut.write(jsonOut)
        fileOut.close()
        

if __name__ == '__main__':
    MrBMM_EmInit.run()