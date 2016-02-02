#!/usr/bin/python

#HW3.4 In this question, we will emit a counter for everytime the reducer is called is called. 
# As we are sorting the data in descending order based on the frequency, we will get the number of baskets on top.
# after that we enter the top 50 product pair in the list and print the record
import sys
import re

sys.stderr.write("reporter:counter:HW3_4b,num_reducers,1\n")

n_max = 50
a_max = []
num_baskets =0 

# input comes from STDIN (standard input)
for line in sys.stdin:
    row = re.split(r'\t+',line.strip())
    freq = int(row[0])
    key = (row[1],row[2])
    
    if(key==('*','NUM_OF_BASKET')):
        num_baskets = freq
        continue
    else:
        # add the lowest 10 words 
        if len(a_max) < n_max:
            a_max.append((key,freq,1.0*freq/num_baskets))
        
for record in a_max:
    print record