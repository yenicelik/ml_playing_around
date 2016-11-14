import numpy as np 
import tensorflow as tf 

class Model():
    def __init__(self, params):
        """ Get parameters and build model """
        #copy the parameters for object saving
        self.params = params
        
        #Define what type of cell we're gonna use
        self.cell = rnn_cell.MultiRNNCell([rnn_cell.BasicLSTM()] * params.num_layers)
        
        #Data input and output
        self.input_data = tf.placeholder(tf.int32, [params.batch_size, params.seq_length])
        self.output_data = tf.placeholder(tf.int32, [params.batch_size, params.seq_length])
        
        #Define the actual model
        self.initial_state = self.cell.zero_state(params.batch_size, tf.float32)
        
        #define a function to define what we do during
        with tf.variable_scope('lstm'):
            #define a namespace, bcs we need to plug one into the seq2seq function
            inp_W = tf.get_variable("softmax_W", [params.rnn_size, params.vocab_size])
            inp_b = tf.get_variable("softmax_b", [params.rnn_size, params.vocab_size])
        
        
        #what specifically does the loop function do differently thatn the dafult function?
        #it may be that the loop function actually stops gradients... but not sure if this is actually the case bcs is stops the gradients for argmax(prev, 1)
        def loop_fn(prev, _):
            prev = tf.matmul(prev, inp_W) + inp_b # sample run
            prev_symbol = tf.stop_gradient(tf.argmax(prev, 1))
            #must return a fckn embeddeding lookup of a fucking symbol
            
        #rest operations (except from recurrent layer)    
        outputs, self.final_state = seq2seq.rnn_decoder(inputs, self.initial_state, self.cell, loop_function=loop_fn, scope='lstm') #do i need to provide a loop function?? documentation says i dont need to
    
        self.scores = tf.matmul(output, inp_W) + inp_b
        self.probs = tf.nn.softmax(self.scores) #calculate probabilites (softmax)
        
        #calculate the loss
        loss = seq2seq.sequence_loss_by_example([self.scores],
                                               [self.output_data],
                                               [tf.ones([params.batch_size * params.seq_length])],
                                               params.vocabl_size
                                               )
        self.cost = tf.reduce_sum(loss) / (params.batch_size*params.seq_length)
        
        #defining the optimization process
        self.lr = tf.Variable(0.0, trainable=False) #wtf, you can train this?!
        optimizer = tf.train.AdamOptimizer(self.lr)
        
        #on how to update the gradients
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tf.trainable_variables()), params.grad_clip)
        self.train_op = optimizer.apply_gradients(zip(grad, tf.trainable_variables()))
        
        
        
        #define here how the characters are converted into one-hot characters
        
    def sample(self):
        """ Generate text from the trained weights etc """
    #model should be able to be saved
        pass