from numpy import argmin, array, random
from mrjob.job import MRJob
from mrjob.step import MRJobStep
from itertools import chain
import numpy as np

#Calculate find the nearest centroid for data point 
def MinDist(datapoint, centroid_points):
    datapoint = array(datapoint)
    centroid_points = array(centroid_points)
    diff = datapoint - centroid_points 
    diffsq = diff*diff
    # Get the nearest centroid for each instance
    minidx = argmin(list(diffsq.sum(axis = 1)))
    return minidx

#Check whether centroids converge
def stop_criterion(centroid_points_old, centroid_points_new,T):
#     return np.alltrue(abs(np.array(centroid_points_new) - np.array(centroid_points_old)) <= T)
    oldvalue = list(chain(*centroid_points_old))
    newvalue = list(chain(*centroid_points_new))
    Diff = [abs(x-y) for x, y in zip(oldvalue, newvalue)]
    Flag = True
    for i in Diff:
        if(i>T):
            Flag = False
            break
    return Flag


class MRKmeans(MRJob):
    centroid_points=[]
    def steps(self):
        return [
            MRJobStep(mapper_init=self.mapper_init,mapper=self.mapper,combiner=self.combiner,reducer=self.reducer)
               ]
    
    #load centroids info from file
    def mapper_init(self):
        self.centroid_points = [map(float,s.split('\n')[0].split(',')) for s in open("Centroids.txt").readlines()]
    
    #load data and output the nearest centroid index and data point 
    def mapper(self, _, line):
        D = line.split(',')
        total = int(D[2])
        code=int(D[1])
        #normalise the input data
        data=map(float,D[3:])
        normalise_data=map(lambda x:((1.0 * x) / total),data)
        yield int(MinDist(normalise_data,self.centroid_points)),(list(normalise_data),1,{code:1})
    
    #Combine sum of data points locally
    def combiner(self, idx, inputdata):
        code = {}
        sum_features= None
        num = 0
        for features,n,codes in inputdata:
            features = array(features)
            if sum_features is None:
                sum_features = np.zeros(features.size)
            sum_features += features
            num += n
            #count codes 
            for k,v in codes.iteritems():
                code[k] = code.get(k,0)+ v
            
        yield idx,(list(sum_features),num,code)
    
    #Aggregate sum for each cluster and then calculate the new centroids
    def reducer(self, idx, inputdata):
        centroids = None
        code = {}
        num = 0
        for features,n,codes in inputdata:
            features = array(features)
           
            if centroids is None:
                centroids = np.zeros(features.size)
            centroids += features 
            
            num += n
            
            #count codes 
            for k,v in codes.iteritems():
                code[k] = code.get(k,0)+v
                
        centroids_new = centroids / num
        yield idx, (list(centroids_new),code)

if __name__ == '__main__':
    MRKmeans.run()