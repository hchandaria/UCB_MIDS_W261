"""Find top 5 most frequenct visited pages.

This program will take input a CSV file of the form 

    V,1000,1,C, 10001
"""
from mrjob.job import MRJob
from mrjob.step import MRJobStep
import csv

def csv_readline(line):
    """Given a sting CSV line, return a list of strings."""
    for row in csv.reader([line]):
        return row

class FreqPages(MRJob):
    def steps(self):
        return [
            MRJobStep(mapper=self.mapper,combiner=self.combiner,reducer=self.reducer),
            MRJobStep(reducer=self.reducer_top5)
               ]

    def mapper(self, line_no, line):
        """Extracts the Vroot that was visited"""
        cell = csv_readline(line)
        yield cell[1],1
                  
    def combiner(self,vroot,visit_counts):
        yield vroot,sum(visit_counts)
    
    def reducer(self, vroot, visit_counts):
        """Sumarizes the visit counts by adding them together."""
        total = sum(i for i in visit_counts)
        yield None, (vroot, total)
                  
    def reducer_top5(self,_,page_counts):
        sorted_list = sorted(list(page_counts),key=lambda x:x[1],reverse=True)[:5]
        for data in sorted_list:
            yield data[0],data[1]
        
if __name__ == '__main__':
    FreqPages.run()