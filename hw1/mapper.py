#!/usr/bin/python
import sys
import re
count = 0
WORD_RE = re.compile(r"[\w']+")
filename = sys.argv[1]
with open (filename, "r") as myfile:
    for line in myfile.readlines():
        #Tokenize each line
        # Split the line by <TAB> delimiter
        content = re.split(r'\t+', line)
        # verify correct content structure else ignore bad data
        if len(content) <> 4:
            continue
        #combine email subject and body
        text = content[2] + ' ' + content[3]
        #tokenize text
        result = re.findall(WORD_RE,text)
        #build a vocabluary of words 
        vocab ={}
        for key in result:
            if key in vocab:
                vocab[key] += 1
            else:
                vocab[key] = 1
        output =content[0]+ "\t" + content[1]
        for key, value in vocab.iteritems():
            output += "\t" + key + "\t" + str(value)
        
        print output