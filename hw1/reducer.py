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
            #get doc id and class of email
            docId = content[0]
            true_class = int(content[1])
            # based on class of email increment spam / non spam count
            if (true_class == 1):
                spam_email_cnt += 1
            else:
                non_spam_email_cnt += 1;
            #if email has content 
            if(len(content) > 2 ):
                #loop through rest of mapper output in increments of 2
                for x in range(2,len(content),2):
                    #get the word and its frequency
                    word = content[x]
                    freq = int(content[x+1])
                    #Determine unique word count for laplace smoothing 
                    if (not(word in spam_words_freq or word in not_spam_words_freq)):
                        unique_word_cnt += 1;
                    #increment spam words, total spam words,ham words, total ham words  based on class of email
                    #
                    if (true_class == 1):
                        total_spam_words += freq;
                        if word in spam_words_freq:
                            spam_words_freq[word] += freq
                        else:
                            spam_words_freq[word] = freq
                        if word not in not_spam_words_freq:
                            not_spam_words_freq[word] = 0
                    else:
                        total_nonspam_words += freq;
                        if word in not_spam_words_freq:
                            not_spam_words_freq[word] += freq
                        else:
                            not_spam_words_freq[word] = freq
                        if word not in spam_words_freq:
                            spam_words_freq[word] = 0

#Calculate prior probabilites for spam and ham
prior_spam = math.log((1.0)*spam_email_cnt / (spam_email_cnt + non_spam_email_cnt ))
prior_ham = math.log((1.0)*non_spam_email_cnt / (spam_email_cnt + non_spam_email_cnt ))
# Condirtional Probability of word given email class spam and ham
pr_word_spam = {}
pr_word_ham = {}
for word in spam_words_freq:
    # 1 is added for laplace smoothing 
    pr_word_spam[word] = pr = math.log((1.0)*(spam_words_freq[word]+1)/ (total_spam_words + unique_word_cnt))
            
for word in not_spam_words_freq:
     # 1 is added for laplace smoothing 
    pr_word_ham[word] = math.log((1.0)*(not_spam_words_freq[word]+1)/ (total_nonspam_words + unique_word_cnt))

#counts for accuracy
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
            if(len(content) > 2 ):
                for x in range(2,len(content),2):
                    word = content[x]
                    freq = int(content[x+1])
                    doc_vocab[word] = freq
            # calculate prob for spam , ham for each email 
            pr_spam_doc = 0.0
            pr_ham_doc = 0.0
            for key,value in doc_vocab.iteritems():
                pr_spam_doc +=  (pr_word_spam[key]*value)
                pr_ham_doc += (pr_word_ham[key]*value)
            #now add prior probabilities for spam and ham
            pr_spam_doc = prior_spam + pr_spam_doc
            pr_ham_doc = prior_ham + pr_ham_doc
            output =  docId+"\t"+true_class+"\t"
            predicted_class = 0
            #Determine the predicted class
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