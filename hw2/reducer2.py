#!/usr/bin/python

from __future__ import division
from itertools import groupby
from operator import itemgetter
import sys
import re
import math


incorrect=0
total = 0

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # Split the value by <TAB> delimiter
    values = re.split(r'\t+', line)

    #Parse the values
    true_class, predicted_class = int(values[1]),int(values[2])
    
    if true_class != predicted_class:#if predicted class is different from true class increment the count
        incorrect+=1
    total += 1
    print line

print "Training error: : %2.3f" %(1.0*incorrect/total)    

    