#!/usr/bin/python
import sys
import re
count = 0
WORD_RE = re.compile(r"[\w']+")
filename = sys.argv[2]
findword = sys.argv[1]
with open (filename, "r") as myfile:
    for line in myfile.readlines():
        #Tokenize each line
        result = re.findall(WORD_RE,line)
        #Now find index of each matching instance of the word
        indices = [i for i,x in enumerate(result) if x.lower() == findword.lower()]
        # increment the count based on the number of occurences found
        count += len(indices)
print count        
#Please insert your code