#!/usr/bin/python
#HW3.2c_1 In this question, we will emit a counter for everytime the reducer is called. 
# In this case of mapreduce we are using secondary sort where in we first sort on the frequency (ascending) 
# and than sort on the issue in case of tie

import sys, Queue
import re
from csv import reader

sys.stderr.write("reporter:counter:Reducer-counter,num_reducers,1\n")

n_max = 50 # top n issues 
n_min = 10 # bottom n issues 
a_min = [] # list to hold the bototom issues 
q_max = Queue.Queue(n_max) # Queue to hold the top 50 issues
total_count =0 

# input comes from STDIN (standard input)
for line in sys.stdin:
    row = re.split(r'\t+',line.strip())
    freq = int(row[0])
    key = row[1]
    #increment the count
    total_count += freq
    
    # add the lowest 10 words as we are getting data in sorted order already
    if len(a_min) < n_min:
        a_min.append((key,freq))
    
    #Now add the top 10 words . In this case we use queue as its FIFO which will always pop the lowest element
    if q_max.full():
        q_max.get()
    q_max.put((key,freq))
    
print '\n Output = Word , Frequency and Relative Frequency'

print '\n%d Bottom issues:' %n_min
for record in a_min:
    print record[0] +"\t"+str(record[1])+"\t"+str(1.0*record[1]/total_count)

print '\n%d Top issues:' %n_max
for i in range(n_max):
    record = q_max.get()
    print record[0] +"\t"+str(record[1])+"\t"+str(1.0*record[1]/total_count)