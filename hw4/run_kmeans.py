
from numpy import random
import numpy as np
from Kmeans import MRKmeans, stop_criterion
import sys
from custom_func import calc_purity
mr_job = MRKmeans(args=['topUsers_Apr-Jul_2014_1000-words.txt'])

random.seed(0)
#number of features
n= 1000

#get centroid type and number of clusters from user
if len(sys.argv) >2: k = int(sys.argv[2])
cen_type = sys.argv[1]

#Geneate initial centroids
centroid_points = []

#based on the centroid type generate centroids
if(cen_type=='Uniform'):
    rand_int = random.uniform(size=[k,n])
    total = np.sum(rand_int,axis=1)
    centroid_points = (rand_int.T/total).T
    with open('Centroids.txt', 'w+') as f:
        f.writelines(','.join(str(j) for j in i) + '\n' for i in centroid_points)
    f.close()
    
elif(cen_type=='Perturbation'):
    data = [s.split('\n')[0].split(',') for s in 
                   open("topUsers_Apr-Jul_2014_1000-words_summaries.txt").readlines()][1]
    #get the total count of words
    total = int(data[2])
    feature = map(lambda x:((1.0 * float(x)) / total),data[3:]) #normalise
    pertubation = feature + random.sample(size=(k,n)) #generate random sample and add it to feature
    sum_per = np.sum(pertubation,axis=1) # calculate the sum to be used for normalization
    centroid_points = (pertubation.T/sum_per).T
    with open('Centroids.txt', 'w+') as f:
        f.writelines(','.join(str(j) for j in i) + '\n' for i in centroid_points)
    f.close()

else:
    data = [s.split('\n')[0].split(',') for s in 
                   open("topUsers_Apr-Jul_2014_1000-words_summaries.txt").readlines()][2:]
    for cluster in data:
        total = 0
        total = int(cluster[2])#get the total count of words
        feature = map(lambda x:((1.0 * float(x)) / total),cluster[3:]) #normalise
        centroid_points.append(feature)
    with open('Centroids.txt', 'w+') as f:
        f.writelines(','.join(str(j) for j in i) + '\n' for i in centroid_points)
    f.close()

print 'Centroid Type: %s' %cen_type
    
# Update centroids iteratively
i = 0
while(1):
    # save previous centoids to check convergency
    centroid_points_old = centroid_points[:]
    print "iteration"+str(i)+":"
    with mr_job.make_runner() as runner: 
        centroid_points = []
        cluster_dist ={}
        runner.run()
        # stream_output: get access of the output 
        for line in runner.stream_output():
            key,value =  mr_job.parse_output_line(line)
            centroid, codes = value
            centroid_points.append(centroid)
            cluster_dist[key]=codes
    i = i + 1
    
    #check if we have convergence
    if(stop_criterion(centroid_points_old,centroid_points,0.001)):
        break
 
    #write new centroids back to file 
    with open('Centroids.txt', 'w') as f:
        for centroid in centroid_points:
            f.writelines(','.join(map(str, centroid)) + '\n')
        f.close()

calc_purity(cluster_dist) 
