#!/usr/bin/python

#HW3.4 In this question, we will emit a counter for everytime the mapper is called is called. 
# In the mapper code we will emit the frequency first followed by the product pair
# we are also going to tell hadoop to sort the key as numeric and in reverse order

import sys
import re

sys.stderr.write("reporter:counter:HW3_4b,num_mappers,1\n")
# input comes from STDIN (standard input)
for line in sys.stdin:
    #remove leading and trailing spaces 
    row = re.split(r'\t',line.strip())
    print '%s\t%s\t%s' %(row[2],row[0],row[1])