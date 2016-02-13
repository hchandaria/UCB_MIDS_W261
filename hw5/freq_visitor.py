"""Find top 5 most frequenct visited pages.

This program will take input a CSV file of the form 

    V,1000,1,C, 10001
"""
from mrjob.job import MRJob
from mrjob.step import MRJobStep
import csv
from mrjob.protocol import RawProtocol, ReprProtocol

def csv_readline(line):
    """Given a sting CSV line, return a list of strings."""
    for row in csv.reader([line]):
        return row

class FreqVisitor(MRJob):
    def steps(self):
        return [
            MRJobStep(mapper=self.mapper1,combiner=self.combiner1,reducer=self.reducer1)
            ,MRJobStep(reducer_init=self.reducer2_init,reducer=self.reducer2)
               ]

    def mapper1(self, line_no, line):
        self.increment_counter('group','num_mapper1_calls',1)
        """Output of mapper is key = (page_id,visitor_id) and value = 1"""
        cell = csv_readline(line)
        yield (cell[1],cell[4]),1
                  
    def combiner1(self,vroot_cust,visit_counts):
        self.increment_counter('group','num_combiner1_calls',1)
        """ Used to do intermediate counts """
        yield vroot_cust,sum(visit_counts)
            
    def reducer1(self, vroot_cust, visit_counts):
        self.increment_counter('group','num_reducer1_calls',1)
        yield vroot_cust[0],(vroot_cust[1],sum(visit_counts))
    
    def reducer2_init(self):
        with open('processed_urls.data') as f:
            self.urls = {k: v for line in f for (k, v) in (line.strip().split(','),)}
    
    def reducer2(self,vroot,value):
        sorted_list = sorted(list(value),key=lambda x:x[1],reverse=True)[:1]
        key = vroot 
        for data in sorted_list:
            yield key,data[0]
    
    
if __name__ == '__main__':
    FreqVisitor.run()