#!/usr/bin/python
import sys
import re
count = 0
WORD_RE = re.compile(r"[\w']+")
filename = sys.argv[1]
findword = sys.argv[2]
with open (filename, "r") as myfile:
    for line in myfile.readlines():
        #Tokenize each line
        # Split the line by <TAB> delimiter
        content = re.split(r'\t+', line)
        # verify correct content structure else ignore bad data
        if len(content) <> 4:
            continue
        text = content[2] + ' ' + content[3]
        result = re.findall(WORD_RE,text)
        #Now find index of each matching instance of the word for that email
        #lower is used to do case insensitive search
        indices = [i for i,x in enumerate(result) if x.lower() == findword.lower()]
        # Correct approach is to increment the count based on the number of occurences found.
        # but shell script example provided only increments once per line matched.
        count += len(indices)
output = findword+"\t"+str(count)
print output        