#!/usr/bin/python
#HW3.2c In this question, we will emit a counter for everytime the combiner is called. 
#the combiner will do intermediate aggregation of data and is similar to reducer in terms of logic
import sys
from csv import reader

sys.stderr.write("reporter:counter:HW_32c,num_combiners,1\n")
last_key = None
word = None
total_count = 0
# input comes from STDIN (standard input)
for token in reader(sys.stdin):
    word=token[0]
    count = int(token[1])
    
    #if current key is same as last_key than increment count 
    if(last_key == word):
        total_count += int(count)
    else:
        if (last_key):
            print '"%s",%s' %(last_key,total_count)
        total_count = int(count)
        last_key = word
if last_key == word:
    print '"%s",%s' %(last_key,total_count)