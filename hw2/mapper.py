#!/usr/bin/python

import sys
import re

WORD_RE = re.compile(r"[\w']+")
       
def main():
    # input comes from STDIN (standard input)
    for line in sys.stdin:
        # remove leading and trailing whitespace
        line = line.strip()
        # Split the line by <TAB> delimiter
        content = re.split(r'\t+', line)
        # verify correct content structure else ignore bad data
        if len(content) <> 4:
            continue
        #Combine email subject and body
        text = content[2] + ' ' + content[3]
        #tokenize email and subject
        result = re.findall(WORD_RE,text)
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        for key in result:
            print '%s\t%s' % (key.lower(), 1)
if __name__ == "__main__":
    main()