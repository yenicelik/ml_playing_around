import numpy as np
from io import StringIO
import os


""" Future ideas:
    * Create Variable Batch Sizes: Transition between batches are then included in modeling the language... any possible good?
"""

class TextLoader():
    """ Helper function to load in (batches of) text """
    
    def __init__(self, batch_size, seq_length, data_dir):
        """ Load data to generate text from. Set batch pointer to zero."""

        input_file = os.path.join(data_dir, "input.txt")
        tensor_file = os.path.join(data_dir, "data.npy")

        if not (os.path.exists(tensor_file)):
            print("reading text file")
        else:
            print("loading files..")
            self.tensor = np.load(tensor_file)

        self.ip = 0 #'insruction' pointer
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.input_file = input_file
        

        with open(self.input_file, 'r') as text_source:
            #self.text = text = np.loadtxt(text_source)
            #print self.text
            self.text = text_source.readlines()[0]
            #print(text)
            #must open up file..
            
            self.chars = list(set(self.text))
            print(sorted(self.chars))
            
            self.vocab_size = len(self.chars)
            print("Vocab size %d" % self.vocab_size)
            
            self.data_size = len(self.text)
            print("Entire data size %d" % self.data_size)
                
        self.map_char2num = { ch:i for i,ch in enumerate(self.chars) }
        self.map_num2char = { i:ch for i,ch in enumerate(self.chars) }
        
        self.num_batches = self.data_size / (self.batch_size * self.seq_length)
        print("Number of batches %d" % self.num_batches)
        self.epochs_through = 0
        
        self.create_batches()

    def create_batches(self):
        """ Creates a number of batches, saved in self.x_batches and self.y_batches"""
        
        if (self.num_batches == 0):
            assert False, "Not enough data to receive batch! :: In function next_batch_pointer of class TextLoader()"
        
        processed_text = self.char2num(self.text)   #turn into numbers 
        processed_text = processed_text[:self.num_batches * self.batch_size * self.seq_length]
        
        x = processed_text
        y = np.zeros(x.shape)
        y[:-1] = np.copy(x[1:])
        y[-1] = np.copy(x[0])
        
        self.X_batches = np.split(x, self.num_batches)
        self.y_batches = np.split(y, self.num_batches)     
        
        
    #################
    #Helper functions
    def char2num(self, char_arr):
        out = np.zeros(len(char_arr), dtype=np.int32)  #will be changed to one-hot anyways... #dtype=float32 if worked on this
        for i in range(out.shape[0]):
            out[i] = self.map_char2num[ char_arr[i] ]
        return out
    
    def num2char(self, num_arr):
        out = ""
        for i in range(num_arr.shape[0]):
            out += self.map_char2num[ num_arr[i] ]
        #out = np.zeros(len(char_arr), dtype=np.int32)  #will be changed to one-hot anyways... #dtype=float32 if worked on this
        return out
    #Helper functions
    #################
    
    
    def get_next_batch(self):
        """ Get next batch of data. This should be a multiple of a sequence 
        length, and a multiple of the batch size """
        x, y = self.X_batches[self.ip], self.y_batches[self.ip]
        self.ip += 1
        if self.ip == self.num_batches:
            self.epochs_through += 1
            print "Epochs through: ", self.epochs_through
            self.reset_batch_pointer()
            
        return x, y
           
    def reset_batch_pointer(self):
        self.ip = 0
        return True
    

if __name__ == "__main__":
    TextLoader = TextLoader(batch_size = 32, 
                            seq_length = 128, #the longer the better
                            data_dir = 'data/dailymail_header/'
                           )
    
    iterations_for_epoch = (TextLoader.data_size) / (TextLoader.batch_size * TextLoader.seq_length) #bcs indexing is from zero...
    print
    print "Iterations through data", iterations_for_epoch
    print
    
    print "Number of batches saved in X_batches:", len(TextLoader.X_batches)
    
    for _ in range(iterations_for_epoch * 10):
        x, y = TextLoader.get_next_batch()
        print x.shape, y.shape
    
        