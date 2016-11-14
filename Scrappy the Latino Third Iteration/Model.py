import numpy as np 
import tensorflow as tf 
from tensorflow.python.ops import rnn_cell
from tensorflow.python.ops import seq2seq
import pip
import os

from tensorflow.python.ops import rnn


class Model():
    def __init__(self, batch_size, seq_length, lstm_size, num_layers, grad_clip, vocab_size):
        """ Build the actual model """
        #Define crucial hyperparameters / parameters
        self.lr = tf.Variable(0.0, trainable=False)        
        
        #Define input and output
        self.input_data = tf.placeholder(tf.int32, [batch_size, seq_length])
        self.output_data = tf.placeholder(tf.int32, [batch_size, seq_length]) #although int would be better for character level..
        
        #Define the model
        cell = tf.nn.rnn_cell.BasicLSTMCell(num_units=lstm_size) #can choose if basic or otherwise later on...
        self.cell = cell = rnn_cell.MultiRNNCell([cell] * num_layers)
        self.initial_state = cell.zero_state(batch_size, tf.float32)
        

        with tf.variable_scope("lstm"):
            softmax_w = tf.get_variable("softmax_w", [lstm_size, vocab_size])
            softmax_b = tf.get_variable("softmax_b", [vocab_size])

            with tf.device("/cpu:0"):
                embedding = tf.get_variable("embedding", [vocab_size, lstm_size])
                inputs = tf.split(1, seq_length, tf.nn.embedding_lookup(embedding, self.input_data))
                inputs = [tf.squeeze(input_, [1]) for input_ in inputs]
        #_, enc_state = rnn.rnn(cell, encoder_inputs, dtype=dtype)
        #outputs, states = rnn_decoder(decoder_inputs, enc_state, cell)

        def loop(prev, _):
            prev = tf.matmul(prev, softmax_w) + softmax_b
            prev_symbol = tf.stop_gradient(tf.argmax(prev, 1))
            return tf.nn.embedding_lookup(embedding, prev_symbol)

        #outputs, last_state

        #outputs, last_state = state_is_tuple=True

        # outputs, states = seq2seq.basic_rnn_seq2seq(
        #                         inputs,
        #                         [self.output_data], 
        #                         cell,
        #                         scope='lstm'
        #                     )
        #print
        #print(len(outputs))
        #print(outputs[0].get_shape())
        #print(type(softmax_w))
        #print(type(softmax_b))
        #print(type(outputs))
        #print(type(self.output_data))
        #print

        #see how attention helps improving this model state...



        # tf.concat([seq_len, batch_size, vocab_size]) 
        # tf.transpose([batch_size, seq_length, vocab_size])



        # #was told that we should actually use samples softmax loss
        # self.loss = tf.nn.sampled_softmax_loss(
        #                                 softmax_w, 
        #                                 softmax_b,
        #                                 outputs, 
        #                                 self.output_data, #bcs this is what tensorflow wants
        #                                 batch_size,
        #                                 vocab_size
        #             )

        outputs, last_state = seq2seq.rnn_decoder(inputs, self.initial_state, cell, loop_function=loop, scope='rnnlm')
        output = tf.reshape(tf.concat(1, outputs), [-1, lstm_size])
        self.logits = tf.matmul(output, softmax_w) + softmax_b
        self.probs = tf.nn.softmax(self.logits)
        loss = seq2seq.sequence_loss_by_example([self.logits],
                [tf.reshape(self.output_data, [-1])],
                [tf.ones([batch_size * seq_length])],
                vocab_size)
        self.cost = tf.reduce_sum(loss) / batch_size / seq_length
        self.final_state = last_state

        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tvars), grad_clip)
        optimizer = tf.train.AdamOptimizer(self.lr)
        self.train_op = optimizer.apply_gradients(zip(grads, tvars)) # what happens for one single iteration



    def sample(self, sess, chars, vocab, num=200, prime='The ', sampling_type=1):
        state = sess.run(self.cell.zero_state(1, tf.float32))
        for char in prime[:-1]:
            x = np.zeros((1, 1))
            x[0, 0] = vocab[char]
            feed = {self.input_data: x, self.initial_state:state}
            [state] = sess.run([self.final_state], feed)

        def weighted_pick(weights):
            t = np.cumsum(weights)
            s = np.sum(weights)
            return(int(np.searchsorted(t, np.random.rand(1)*s)))

        ret = prime
        char = prime[-1]
        for n in range(num):
            x = np.zeros((1, 1))
            x[0, 0] = vocab[char]
            feed = {self.input_data: x, self.initial_state:state}
            [probs, state] = sess.run([self.probs, self.final_state], feed)
            p = probs[0]

            if sampling_type == 0:
                sample = np.argmax(p)
            elif sampling_type == 2:
                if char == ' ':
                    sample = weighted_pick(p)
                else:
                    sample = np.argmax(p)
            else: # sampling_type == 1 default:
                sample = weighted_pick(p)

            pred = chars[sample]
            ret += pred
            char = pred
        return ret



if __name__ == "__main__":
    
    Model = Model(batch_size=32, 
                  seq_length=128, 
                  lstm_size=512, 
                  num_layers=2, 
                  grad_clip=5,
                  vocab_size=82
                 )
