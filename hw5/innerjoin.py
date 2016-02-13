
from mrjob.job import MRJob
from mrjob.step import MRJobStep
import csv, re
from mrjob.protocol import RawProtocol, ReprProtocol

class InnerJoin(MRJob):
    def steps(self):
        return [
            MRJobStep(mapper_init=self.mapper_init, mapper=self.mapper)
               ]
    
    def mapper_init(self):
        with open('most_visitors.out') as f:
            self.left = {k: v for line in f for (k, v) in (line.replace('"', '').strip().split('\t'),)}
        
    
    def mapper(self, line_no, line):
        cell = line.strip().split(',')
        url = self.left.get(cell[0],'NA')
        if url != 'NA':
            yield cell[0], (cell[1],self.left.get(cell[0],'NA'))
                   
if __name__ == '__main__':
    InnerJoin.run()