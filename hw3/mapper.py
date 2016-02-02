#!/usr/bin/python
import sys
import re

sys.stderr.write("reporter:counter:HW3_5a,num_mappers,1\n")
# input comes from STDIN (standard input)
for line in sys.stdin:
    # Emit * , BAKSET for counting total number of baskets 
    print '%s\t%s\t%s'%('*','BASKET',1)
    # remove leading and trailing whitespace and tokenize
    token  =  line.strip().split(" ")
    uniq_tokens = sorted(set(token))
    for i in range (0,len(uniq_tokens)-1):
        key = uniq_tokens[i]
        value = ""
        for j in range(i+1, len(uniq_tokens)):
            value += uniq_tokens[j] + "\t1\t"
        print '%s\t%s' %(key,value)