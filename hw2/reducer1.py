#!/usr/bin/python

from itertools import groupby
from operator import itemgetter
import sys
import re
import math

spam_email_cnt  = 0 # Total count of spam emails 
ham_email_cnt = 0 #Total count of non spam emails 
total_spam_words = 0 #Total count of words in all spam emails 
total_ham_words = 0 # Total count of words in all non spam emails 
spam_words_freq = {} # Dictionary to store overall frequency of words for spam emails
ham_words_freq ={} # Dictionary to store overall frequency of words for non spam emails
unique_word_cnt = 0 # Unique vocab length

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    key, value = line.split(',', 1)
    
    if(key =="DOC_CLASS"):
        #increment spam or ham count 
        spam_email_cnt += int(value)
        ham_email_cnt += not(int(value))
        continue
    
    # Split the value by <TAB> delimiter
    values = re.split(r'\t+', value)

    #Parse the values
    true_class,freq = int(values[0]), int(values[1])
    word = key
    
    #Determine unique word count for laplace smoothing 
    if (not(word in spam_words_freq or word in ham_words_freq)):
        unique_word_cnt += 1;
    
    #increment spam words, total spam words,ham words, total ham words  based on class of email
    if (true_class == 1):
        total_spam_words += freq;
        if word in spam_words_freq:
            spam_words_freq[word] += freq
        else:
            spam_words_freq[word] = freq
        if word not in ham_words_freq:
            ham_words_freq[word] = 0
    else:
        total_ham_words += freq;
        if word in ham_words_freq:
            ham_words_freq[word] += freq
        else:
            ham_words_freq[word] = freq
        if word not in spam_words_freq:
            spam_words_freq[word] = 0

#Now calculate prior probabilities for spam & ham
p_sp = (1.0)*spam_email_cnt / (spam_email_cnt + ham_email_cnt )
prior_spam = math.log(p_sp)
prior_ham = math.log(1-p_sp)

print "OVERALL,"+str(prior_spam)+","+str(prior_ham)

# Calculate Conditional Probability of word given email class spam and ham
pr_word_spam = {}
pr_word_ham = {}

#if frequency of word is less than 3 ignore the word from vocab 
for word in ham_words_freq:
    if( (ham_words_freq[word]+spam_words_freq[word])<3):
        unique_word_cnt -= 1

#if frequency of word is less than 3 ignore the word and do not calculate the propability
for word in ham_words_freq:
    if( (ham_words_freq[word]+spam_words_freq[word])<3):
        continue
    #One is added here to do LapLace smoothing
    pr_word_spam[word] = math.log((1.0)*(spam_words_freq[word]+1)/ (total_spam_words + unique_word_cnt))     
    pr_word_ham[word] = math.log((1.0)*(ham_words_freq[word]+1)/(total_ham_words + unique_word_cnt))
    print word+","+str(pr_word_spam[word])+","+str(pr_word_ham[word])