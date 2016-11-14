import codecs
import os
import collections
from six.moves import cPickle
import numpy as np 

class TextLoader():
	""" A class to retrieve text, split it into batches, and provide them to the learning algorithm """
	
	def __init__(self, data_dir, batch_size, seq_length, encoding='utf-8'):
		self.data_dir = data_dir
		self.batch_size = batch_size
		self.seq_length = seq_length
		self.encoding = encoding

		input_file = os.path.join(data_dir, "input.txt")
		vocab_file = os.path.join(data_dir, "vocab.pkl") #where we save.. what exactly?
		tensor_file = os.path.join(data_dir, "data.npy") #where we save.. what exactly?

		#if vocab_file and tensor_file is not yet created, create it now
		if not (os.path.exists(vocab_file) and os.path.exists(tensor_file)):
			print("reading text file")
			self.preprocess(input_file, vocab_file, tensor_file)
		else:
			print("loading preprocessed files")
			self.load_preprocessed(vocab_file, tensor_file)
		self.create_batches()
		self.reset_batch_pointer()


	#Opt1: Running model from scratch
	def preprocess(self, input_file, vocab_file, tensor_file):
		with codecs.open(input_file, "r", encoding=self.encoding) as f:
			data = f.read()
		counter = collections.Counter(data)
		count_pairs = sorted(counter.items(), key=lambda x: -x[1]) 							#sorts all characters by frequency
		self.chars, _ = zip(*count_pairs) 													#all different characters in a list (no mapping!)
		self.vocab_size = len(self.chars) 													#how many disctinct characters we have..
		self.vocab = dict(zip(self.chars, range(len(self.chars)))) 							#the different characters in a dictionary (mapping character to number)
		with open(vocab_file, 'wb') as f:
			cPickle.dump(self.chars, f)
		self.tensor = np.array(list(map(self.vocab.get, data))) 							#self.tensor is the actual data (in numbers)
		np.save(tensor_file, self.tensor)



	#Opt2: Continuing model from previous model
	def load_preprocessed(self, vocab_file, tensor_file):
		with open(vocab_file, 'rb') as f:
			self.chars = cPickle.load(f)
		self.vocab_size = len(self.chars)
		self.vocab = dict(zip(self.chars, range(len(self.chars))))
		self.tensor = np.load(tensor_file)
	

	def create_batches(self):
		self.num_batches = self.tensor.size / self.batch_size / self.seq_length

		if self.num_batches == 0:
			assert False, "Not enough data"

		self.tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length] #discretised
		x_data = self.tensor
		y_data = np.copy(self.tensor)
		y_data[:-1] = x_data[1:]
		y_data[-1] = x_data[0]
		self.x_batches = np.split(x_data.reshape(self.batch_size, -1), self.num_batches, 1)
		self.y_batches = np.split(y_data.reshape(self.batch_size, -1), self.num_batches, 1)

		#validation and test sets as next steps?

	def next_batch(self):
		#if self.pointer is out of range, increment the epoch count, and reset batch pointer
		x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
		self.pointer += 1
		return x, y

	def reset_batch_pointer(self):
		self.pointer = 0


if __name__ == "__main__":
	data_loader = TextLoader(
		data_dir = "data/dailymail_header/",
		batch_size = 32,
		seq_length = 128,
		)

	for i in range(50):
		x, y = data_loader.next_batch()
		print
		print x.shape