#!/usr/bin/python

#HW3.4 In this question, we will emit a counter for everytime the reducer is called. 
# In this reducer code we aggregate the basket count and products that occur together.

import sys
import re


sys.stderr.write("reporter:counter:HW3_4,num_reducers,1\n")
last_key = None
word = None
total_count = 0
max_basket = -1
basket_cnt = 0
sup_cnt = 0 
# input comes from STDIN (standard input)
for line in sys.stdin:
    row = re.split(r'\t+',line.strip())
    product = (row[0],row[1]) #combine product1 and product2 as tuple to be used as key
    count = int(row[2])
    #increment total number of baskets if incoming data is for baskets 
    if (product ==('*','BASKET')):
        basket_cnt += count
        continue
    #increment the count for products that occur together
    else:    
        #if current key is same as last_key than increment count 
        if(last_key == product):
            total_count += count
        else:
            #emit pair of product if they are greater than 100
            if (last_key and total_count > sup_cnt):
                print '%s\t%s\t%s' %(last_key[0],last_key[1],total_count)
            total_count = count
            last_key = product
if (last_key == product and total_count > sup_cnt ):
    print '%s\t%s\t%s' %(last_key[0],last_key[1],total_count)
#emit the total number of baskets
print '%s\t%s\t%s' %('*','NUM_OF_BASKET',basket_cnt)
