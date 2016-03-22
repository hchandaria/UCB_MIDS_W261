from __future__ import division
from mrjob.job import MRJob
from mrjob.step import MRStep

# This MrJob calculates the gradient of the entire training set 
#     Mapper: calculate partial gradient for each example  

class MRJob_GD_LR(MRJob):
    def steps(self):
        return [MRStep(mapper_init=self.read_weights,
                       mapper=self.partial_gradient,
                       mapper_final=self.partial_gradient_emit,
                       reducer=self.gradient_accumulater,
                       jobconf={
                        "mapred.map.tasks":4,
                        "mapred.reduce.tasks":1
                        }
                      )] 
    
    def read_weights(self):
        # Read initial_seed file
        with open('initial_seed.txt', 'r') as f:
            self.seed = [float(v) for v in f.readline().split(',')]
        # Initialze gradient for this iteration
        self.partial_Gradient = [0]*len(self.seed)
        self.partial_count = 0
    
    def partial_gradient(self,_,line):
        y_l,x_l = map(float,line.split(','))
        #assume equation is of the form y=b0+b1x. Get values of b0 and b1 from the intial seed
        b0,b1 = self.seed
        
        #calculate weight as abs(1/x)
        w_l = abs(1/x_l)
        
        # y_hat is the predicted value given current weights
        y_hat = b0+b1*x_l
        
        # Update parial gradient vector with gradient form current example
        self.partial_Gradient =  [self.partial_Gradient[0]+ (y_l-y_hat)*w_l, self.partial_Gradient[1]+(y_l-y_hat)*x_l*w_l]
        self.partial_count = self.partial_count + 1
        #yield None, (D[0]-y_hat,(D[0]-y_hat)*D[1],1)
    
    # Finally emit in-memory partial gradient and partial count
    def partial_gradient_emit(self):
        yield None, (self.partial_Gradient,self.partial_count)
        
    # Accumulate partial gradient from mapper and emit total gradient 
    # Output: key = None, Value = gradient vector
    def gradient_accumulater(self, _, partial_Gradient_Record): 
        total_gradient = [0]*2
        total_count = 0
        for partial_Gradient,partial_count in partial_Gradient_Record:
            total_count = total_count + partial_count
            total_gradient[0] += partial_Gradient[0]
            total_gradient[1] +=partial_Gradient[1]
        yield None, [v/total_count for v in total_gradient]
    
if __name__ == '__main__':
    MRJob_GD_LR.run()