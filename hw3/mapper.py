#!/usr/bin/python
#HW3.2c_1 In this question, we will emit a counter for everytime the mapper is called. 
# output of mapper is frequency and issue 
# output of previous mapreduce job is used as input for this map reduce task
import sys
from csv import reader

sys.stderr.write("reporter:counter:Mapper-counter,num_mappers,1\n")

# input comes from STDIN (standard input)
for token in reader(sys.stdin):
    print '%s\t"%s"' %(token[1],token[0])