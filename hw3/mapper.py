#!/usr/bin/python

#hw3.5b 

import sys
import re

sys.stderr.write("reporter:counter:HW3_5b,num_mappers,1\n")
# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace and tokenize
    token  =  line.strip().split("\t")
    for i in range (0,len(uniq_tokens)-1):
        key = uniq_tokens[i]
        value = ""
        for j in range(i+1, len(uniq_tokens)):
            value += uniq_tokens[j] + "\t1\t"
        print '%s\t%s' %(key,value)