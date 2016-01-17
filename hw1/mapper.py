#!/usr/bin/python
import sys
import re
count = 0
WORD_RE = re.compile(r"[\w']+")
filename = sys.argv[1]
findwords ={}
vocab_len = len(sys.argv[2:])
for word in sys.argv[2:]:
    findwords[word] = 1
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
        #build a vocabluary of words 
        vocab ={}
        for key in result:
            if key not in findwords:
                continue
            if key in vocab:
                vocab[key] += 1
            else:
                vocab[key] = 1
        output =content[0]+ "\t" + content[1]+"\t"+str(len(result))+"\t"+str(vocab_len)
        for key, value in vocab.iteritems():
            output += "\t" + key + "\t" + str(value)
        
        print output