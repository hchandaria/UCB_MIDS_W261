#!/usr/bin/python
#H3.5 This reducer functions gets the total number of baskets as the first element from mapper due to 
# which we are able to use it to calculate relative frequncy. I have used heapq to insert top 100 products. 
# This code was written before we got instructions to use 2 map reduce jobs. I have not removed this piece of code. 
# Given that we need to sort data based  lexicographically the 2nd map reduce job helps with it.


import sys
import re
import heapq
import operator

sys.stderr.write("reporter:counter:HW3_5a,num_reducers,1\n")

last_key = None
word = None
total_count = 0
max_basket = -1
basket_cnt = 0 
sup_cnt = 100 # variable to hold the minimum support count 
tmp_dict ={} # for aggregation
n_max = 100 # top n product pairs 
max_q = []

#function to add to queue.
#we have used heapq here so we can remove the smallest element if the queue is full during insertion.
def add_to_max_Q(p1,p2,cnt):
    # add elements if q is not full
    if (len(max_q) < n_max):
        heapq.heappush(max_q, (cnt, (p1,p2)))
    else:
        # add new element and then remove smallest element
        heapq.heappush(max_q, (cnt, (p1,p2)))
        heapq.heappop(max_q)
    
#function to print the queue data
def print_topn(total_bsk):
    cnt = len(max_q)
    if(cnt > n_max):
        cnt = n_max
    s = heapq.nlargest(cnt, max_q)
    for row in s:
        print '%s\t%s\t%s\t%s'%(row[1][0] ,row[1][1],row[0],(1.0*row[0]/total_bsk))

def merge_dict(merged,row):
    for product in row:
        if product in merged:
            merged[product] += row[product]
        else:
            merged[product] = row[product]
    return merged

def emit_dict(key,merged):
    output = key
    cnt =0
    merged_sorted = sorted(merged.items(), key=operator.itemgetter(0))
    for tup in merged_sorted:
        # for prd, value in merged_sort.iteritems():
        prd = tup[0]
        value = tup[1]
        if(value < sup_cnt):
            continue
        cnt += 1
        add_to_max_Q(key,prd,value)
        output += "\t" + prd + "\t" + str(value)

# input comes from STDIN (standard input)
for line in sys.stdin:
    row = re.split(r'\t',line.strip())
    product = row[0]
    #increment the total basket if we encounter * BASKET tuple
    if(row[0]=='*' and row[1]=='BASKET'):
        basket_cnt += int(row[2])
        
        continue
        
    #increment the count for products that occur together. 
    else:
        row_dict ={}
        #parse the remaining data elements and increment counters by 2
        for x in range (1,len(row),2):
            prd = row[x]
            prd_cnt = int(row[x+1])
            row_dict[prd]=prd_cnt
        
        if(last_key == product):
            #update dictionary                
            tmp_dict=merge_dict(tmp_dict,row_dict)

        #emit the data is we find new product key 
        else:
            #emit pair of product if they are greater than 100
            if (last_key):
                #print dictionary
                emit_dict(last_key,tmp_dict)
            #create dictonary
            tmp_dict=row_dict
            last_key = product
                        
            
if (last_key == product):
    #print dictionary
    emit_dict(last_key,tmp_dict)
    
#emit the total number of baskets
print '%s\t%s\t%s\t%s' %('*','NUM_OF_BASKET',basket_cnt,1)     
# "\n %d Top product pairs that occur together" %(n_max)
print_topn(basket_cnt)