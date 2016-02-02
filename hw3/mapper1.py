#!/usr/bin/python
#HW3.4 In this question, we will emit a counter for everytime the mapper is called. 
# In this mapper code, we are first taking unique products for each basket ( if there are duplicates ) 
# and than sorting it. We have used python function of combinations to emit all tuples of length 2.
# We also emit for everyline read a count for the number of baskets 

import sys
import re
import itertools

sys.stderr.write("reporter:counter:HW3_4,num_mapper,1\n")
# input comes from STDIN (standard input)
for line in sys.stdin:
    # emit count for basket
    print '%s\t%s\t%s'%('*','BASKET',1)
    
    # remove leading and trailing whitespace and tokenize
    token  =  line.strip().split(" ")
    for subset in itertools.combinations(sorted(set(token)), 2):
        print '%s\t%s\t%s' % (subset[0],subset[1], 1)
    