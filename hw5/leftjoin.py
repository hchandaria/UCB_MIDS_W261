
from mrjob.job import MRJob
from mrjob.step import MRJobStep
import csv, re
from mrjob.protocol import RawProtocol, ReprProtocol

class LeftJoin(MRJob):
    left ={}
    left_seen = {}
    def steps(self):
        return [
            MRJobStep(mapper_init=self.mapper_init, mapper=self.mapper,mapper_final = self.mapper_final)
               ]
    
    def mapper_init(self):
        with open('most_visitors.out') as f:
            self.left = {k: v for line in f for (k, v) in (line.replace('"', '').strip().split('\t'),)}
        self.left_seen = dict.fromkeys(self.left, 0)
    
    def mapper(self, line_no, line):
        cell = line.strip().split(',')
        cust_id = self.left.get(cell[0],'NA')
        if cust_id != 'NA':
            self.left_seen[cell[0]] = 1
            yield cell[0], (cell[1],cust_id)
    
    def mapper_final(self):
        for pageid, seen in self.left_seen.iteritems():
            if seen == 1:
                continue
            yield pageid, (self.left.get(pageid),'NULL')
                
                   
if __name__ == '__main__':
    LeftJoin.run()