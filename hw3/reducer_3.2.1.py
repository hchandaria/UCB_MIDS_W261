#!/usr/bin/python
from __future__ import division # Use Python 3-style division
import sys, Queue, csv

sys.stderr.write('reporter:counter:custom,reducer_called,1\n')
    
wordCount = 0 # Count of each word
totalCount = 0 # Total number of words
curr = None # the current word

# input format: 
# Total count: group \t count \t max.int
# Word: group \t word \t count
for fields in csv.reader(sys.stdin, delimiter='\t'):
    group = fields[0]
    word = fields[1]
    count = fields[2]
    count = int(count)

    # Find out the total word count.
    # We use count == sys.maxint as the special key for order inversion.
    if count == sys.maxint:
        totalCount += int(word) # The word is the count
        continue
    
    # If we have encountered a new word, output the answer of the current word
    if curr != word:
        if curr is not None:
            print "\t".join([curr, str(wordCount), str(wordCount/totalCount)])
            wordCount = 0
            
    wordCount += count
    curr = word

# Handle the last word seen
if curr is not None:
    print "\t".join([curr, str(wordCount), str(wordCount/totalCount)])