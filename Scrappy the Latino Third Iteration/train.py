import numpy as np 
import tensorflow as tf 

import time
import os


from Model import Model

def train(num_epochs, learning_rate, decay_rate, batch_size, seq_length, input_file, lstm_size, num_layers, init_from=None, save_every=1000):
	import TextLoader
	TextLoader = TextLoader.TextLoader(batch_size=batch_size, seq_length=seq_length, data_dir=input_file)
	iterations_for_epoch = (TextLoader.data_size) / (TextLoader.batch_size * TextLoader.seq_length)

	###################################
	#Importing the last trained model #
	###################################
	# check compatibility if training is continued from previously saved model
	ckpt = None
	if init_from is not None:
		# check if all necessary files exist 
		assert os.path.isdir(init_from)," %s must be a a path" % init_from
		ckpt = tf.train.get_checkpoint_state(init_from)
		assert ckpt,"No checkpoint found"
		assert ckpt.model_checkpoint_path,"No model path found in checkpoint"

	###################################
	#Importing the last trained model #
	###################################


	model = Model(batch_size=batch_size, 
				  seq_length=seq_length, 
				  lstm_size=lstm_size, 
				  num_layers=num_layers, 
				  grad_clip=5,
				  vocab_size=TextLoader.vocab_size)


	with tf.Session() as sess:
		tf.initialize_all_variables().run()

		saver = tf.train.Saver(tf.all_variables())
		if(init_from is not None):
			saver.restore(sess, ckpt.model_checkpoint_path)

		#check again what substitutes one epoch...
		for e in range(num_epochs):
			tf.assign(model.lr, learning_rate * (decay_rate ** e))
			TextLoader.reset_batch_pointer()
			state = sess.run(model.initial_state) #why initial_state?...

			for b in range(TextLoader.num_batches):
				start = time.time()
				x, y = TextLoader.get_next_batch()
				x = x.reshape((batch_size, seq_length))
				y = y.reshape((batch_size, seq_length))
				#print("x shape: ", x.shape)
				feed = {
						model.input_data: x, 
						model.output_data: y, 
						model.initial_state: state
						}
				train_loss, state, _ = sess.run([model.cost, model.final_state, model.train_op], feed)
				end = time.time()
				print("{}/{} (epoch {}), train_loss = {:.3f}, time/batch = {:.3f}" \
					.format(e * TextLoader.num_batches + b, num_epochs * TextLoader.num_batches, e, train_loss, end - start))


	###################################
	#  Saving the last trained model  #
	###################################

				if (e * TextLoader.num_batches + b) % save_every == 0 or (e==num_epochs-1 and b == TextLoader.num_batches-1):
					checkpoint_path = os.path.join(input_file, 'model.ckpt')
					saver.save(sess, checkpoint_path, global_step = e * TextLoader.num_batches + b)
					print("model saved to {}".format(checkpoint_path))
				
	###################################
	#  Saving the last trained model  #
	###################################
	


if __name__ == "__main__":
	train(
		num_epochs = 50, #50
		learning_rate = 1e-3, #1e-3 
		decay_rate = 0.97, #0.97
		batch_size = 32, #50
		seq_length = 64, #50 
		input_file = 'data/dailymail_header/',
		lstm_size=512,
		num_layers = 2,
		save_every = 10, #1000
		init_from='data/dailymail_header/' 
		#save_every, init_from, save_dir,
		)
