#!/usr/bin/python
import sys
import re
import csv
import numpy as np

# The input is the result from hw3.2-part3, which has the format:
# word<tab>count

n = 0
rate = 5 # sample one out of every five counts
samples = []

# We want to sample the count
for line in sys.stdin:
    (word, count) = line.strip().split(",")

    if n % rate == 0:
        samples.append(int(count))
        
    n += 1
    
# Now we have a sample of counts.  Let's find the 50% percentile, as we only have 2 reducers.
p50 = np.percentile(samples, 50)

print p50