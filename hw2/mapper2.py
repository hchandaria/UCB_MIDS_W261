#!/usr/bin/python
# Mapper for HW 2.4
# This mapper will 
    
import sys
import re
import csv


WORD_RE = re.compile(r"[\w']+")
pr_cc_word={}

#Read the model parameters 
data = None
with open('Model_24.txt', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        if(row[0]=="OVERALL"):
            prior_spam = float(row[1])
            prior_ham = float(row[2])
            continue
        pr_cc_word[row[0]]={'spam':float(row[1]),'ham':float(row[2])}

        

#input comes from STDIN (standard input)
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
        
        pr_spam_doc = prior_spam
        pr_ham_doc = prior_ham
        for w in result:
            word = w.lower()
            # calculate prob for spam , ham for each email
            if(word not in pr_cc_word):
                continue
            pr_spam_doc +=  pr_cc_word[word]['spam']
            pr_ham_doc += pr_cc_word[word]['ham']

        predicted_class = "0"
        #Determine the predicted class
        if(pr_spam_doc == float('-inf')) :
            predicted_class = "0"
        elif(pr_ham_doc == float('-inf')):
            predicted_class = "1"
        elif(pr_spam_doc > pr_ham_doc):
            predicted_class = "1"
        
        #prepare the value output 
        value = content[1]+"\t" + predicted_class+ "\t" + str(pr_spam_doc)+ "\t" +str(pr_ham_doc)
        
        #emit key. value combination
        print content[0] + "\t" + value