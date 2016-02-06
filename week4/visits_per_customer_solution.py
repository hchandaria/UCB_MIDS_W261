"""Find Vroots with more than 400 visits.

This program will take a CSV data file and output tab-seperated lines of

    Custermer -> number of visits

To run:

    python visits_per_customer_solution.py processed_anonymous-msweb.data

To store output:

    python visits_per_customer_solution.py processed_anonymous-msweb.data > visits_per_customer_solution.out
"""

from mrjob.job import MRJob
import csv

def csv_readline(line):
    """Given a sting CSV line, return a list of strings."""
    for row in csv.reader([line]):
        return row

class CustomerVisit(MRJob):

    def mapper(self, line_no, line):
        """Extracts the Customer that visit a page"""
        cell = csv_readline(line)
        if cell[0] == 'V':
            yield cell[4],1

    def reducer(self, customer, visit_counts):
        """Sumarizes the visit counts by adding them together."""
        total =0
        total = sum(i for i in visit_counts)
        yield customer,total
        
if __name__ == '__main__':
    CustomerVisit.run()