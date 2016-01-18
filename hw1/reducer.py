#!/usr/bin/python
import sys
import re
import math 
sum = 0
# Dictionary to store overall frequency of words for spam emails 
spam_words_freq = {}
# Dictionary to store overall frequency of words for non spam emails 
not_spam_words_freq ={}
# Total count of spam emails 
spam_email_cnt  = 0
# Total count of non spam emails 
non_spam_email_cnt = 0
# Unique vocab length
unique_word_cnt = 0
#Total count of words in all spam emails 
total_spam_words = 0
# Total count of words in all non spam emails 
total_nonspam_words = 0
for x in range(1,len(sys.argv)):
    with open (sys.argv[x], "r") as myfile:
        for line in myfile.readlines():
            # Split the line by <TAB> delimiter
            content = re.split(r'\t+', line)
            docId = content[0]
            true_class = int(content[1])
            doc_word_cnt = int(content[2])
            unique_word_cnt = int(content[3])
            if (true_class == 1):
                spam_email_cnt += 1
                total_spam_words += doc_word_cnt
            else:
                non_spam_email_cnt += 1
                total_nonspam_words += doc_word_cnt
            if(len(content) > 4 ):
                for x in range(4,len(content),2):
                    word = content[x]
                    freq = int(content[x+1])
                    if (true_class == 1):
                        if word in spam_words_freq:
                            spam_words_freq[word] += freq
                        else:
                            spam_words_freq[word] = freq
                    else:
                        if word in not_spam_words_freq:
                            not_spam_words_freq[word] += freq
                        else:
                            not_spam_words_freq[word] = freq
                            
prior_spam = math.log((1.0)*spam_email_cnt / (spam_email_cnt + non_spam_email_cnt ))
prior_ham = math.log((1.0)*non_spam_email_cnt / (spam_email_cnt + non_spam_email_cnt ))
# Probability of word given email class spam 
pr_word_spam = {}
pr_word_ham = {}
for word in spam_words_freq:
    if(spam_words_freq[word] > 0 ):
        pr_word_spam[word] = math.log((1.0)*(spam_words_freq[word])/ (total_spam_words))
    else:
        pr_word_spam[word] = float('-inf')
for word in not_spam_words_freq:
    if(not_spam_words_freq[word] > 0):
        pr_word_ham[word] = math.log((1.0)*(not_spam_words_freq[word])/(total_nonspam_words))
    else:
        pr_word_ham[word] = float('-inf')

correct_match_cnt = 0
total_match = 0
###### Classification ########## 
for x in range(1,len(sys.argv)):
    with open (sys.argv[x], "r") as myfile:
        for line in myfile.readlines():
            # Split the line by <TAB> delimiter
            content = re.split(r'\t+', line)
            docId = content[0]
            true_class = content[1]
            doc_vocab = {}
            if(len(content) > 4 ):
                for x in range(4,len(content),2):
                    word = content[x]
                    freq = int(content[x+1])
                    doc_vocab[word] = freq
            # calculate prob for spam , ham
            pr_spam_doc = 0.0
            pr_ham_doc = 0.0
            for key,value in doc_vocab.iteritems():
                if (pr_word_spam[key] == float('-inf')):
                    if(value !=0):
                        pr_spam_doc += float('-inf')
                    else :
                        pr_spam_doc += 0
                else:   
                    pr_spam_doc += (pr_word_spam[key]*value)
                if(pr_word_ham[key] == float('-inf')):
                    if(value !=0):
                        pr_ham_doc += float('-inf')
                    else :
                        pr_ham_doc += 0
                else :
                    pr_ham_doc += (pr_word_ham[key]*value)                 
            pr_spam_doc = prior_spam + pr_spam_doc
            pr_ham_doc = prior_ham + pr_ham_doc
            output =  docId + "\t" + true_class + "\t"
            predicted_class = 0
            if(pr_spam_doc > pr_ham_doc) :
                predicted_class = 1
                output += "1"
            else:
                output += "0"
            if(int(true_class) == predicted_class):
                correct_match_cnt += 1
            total_match += 1
            print output 
print "Accuracy of the model: %3.2f" %(correct_match_cnt*100.0/total_match) 