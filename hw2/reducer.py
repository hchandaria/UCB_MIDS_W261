#!/usr/bin/python

from itertools import groupby
from operator import itemgetter
import sys

def main():
    last_key = None
    word = None
    total_count = 0
    # input comes from STDIN (standard input)
    for line in sys.stdin:
        # remove leading and trailing whitespace
        line = line.strip()

        # parse the input we got from mapper.py
        word, count = line.split('\t', 1)

        #if current key is same as last_key than increment count 
        if(last_key == word):
            total_count += int(count)
        else:
            if (last_key):
                # write result to STDOUT
                print '%s\t%s' %(last_key,total_count)
            total_count = int(count)
            last_key = word
    if last_key == word:
        print '%s\t%s' %(last_key,total_count)

if __name__ == "__main__":
    main()