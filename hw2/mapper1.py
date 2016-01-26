#!/usr/bin/python
#Mapper how Hw1.3.
# This mapper will go through each email and emit the count of each word alng with document class
import sys
import re
count = 0
WORD_RE = re.compile(r"[\w']+")

 
# input comes from STDIN (standard input)
for line in sys.stdin:
        # Split the line by <TAB> delimiter
        content = re.split(r'\t+', line)
        # verify correct content structure else ignore bad data
        if len(content) <> 4:
            continue
        #combine email subject and body  and remove leading and trailing spacers
        text = " ".join(content[-2:]).strip()
        # Find all words
        result = re.findall(WORD_RE,text)

        #build a vocabluary of words 
        vocab ={}
        for w in result:
            word = w.lower()
            if word in vocab:
                vocab[word] += 1
            else:
                vocab[word] = 1
                
        doc_class = content[1]       
        for key, value in vocab.iteritems():
            print key + "," +str(doc_class)+"\t" +str(value)
            
        #emit SPAM or HAM for document counts 
        print "DOC_CLASS,"+str(doc_class) 