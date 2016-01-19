#!/usr/bin/python
import sys
import re
sum = 0
for x in range(1,len(sys.argv)):
    with open (sys.argv[x], "r") as myfile:
        for line in myfile.readlines():
            #Please insert your code
            #convert to int and increment the sum
            content = re.split(r'\t+', line)
            sum += int(content[1])   
print content[0]+"\t"+str(sum)