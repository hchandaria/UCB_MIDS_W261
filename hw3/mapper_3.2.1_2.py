#!/usr/bin/python
import sys
import re
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--partitionFile", default="partitions.txt")

args = parser.parse_args()

sys.stderr.write('reporter:counter:custom,mapper_called,1\n')


# The input is the result from hw3.2-part3, which has the format:
# word<tab>count

# First read the partition file and get the 50th percentile
with open(args.partitionFile, 'r') as f:
    p50 = float(f.readline())

groups = ["g" + str(x) for x in range(2)] # names of the two groups

for line in sys.stdin:
    (word, count) = line.strip().split(",")
    count = int(count)

    # Assign it to different reducers based on the count value
    if count >= p50:
        group = groups[0]
    else:
        group = groups[1]
        
    print group + "\t" + word+"\t"+str(count)

    # Use order inversion so that reducer can count the total word count in a single pass
    # Need to send it to each group
    for g in groups:
        print g + "\t" + str(count) + "\t" + str(sys.maxint)