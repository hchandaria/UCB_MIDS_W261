#!/usr/bin/python
""" This program process the log file and outputs 2 separate files. 
    One for the log information and other is page URLS's.
"""
import sys
import re

inputfile = sys.argv[1]
outputfile = open('processed_anonymous-msweb.data', 'a')
outputfile2 = open('processed_urls.data', 'a')

for line in open(inputfile):
    v = line.split(',')
    # If the line is customer information line, save it to customer_info
    if(v[0]=='C'):
        customer_info = v
    # If the line visit information line, concatenate the line with customer_info
    elif(v[0]=='V'):
        outputfile.write( line.strip()+','+customer_info[0]+','+customer_info[1].strip('"')+'\n')
    # Directly output other lines
    elif(v[0]=='A'):
        outputfile2.write(v[1]+','+ re.sub(r'\"+','',v[4]))
    else:
         continue