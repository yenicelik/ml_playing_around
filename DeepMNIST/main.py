from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf


mnist = input_data.read_data_sets('MNIST_data', one_hot = True)


#Start to build the computational graph
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.matmul(x, W) + b


sess = tf.InteractiveSession()
tf.initialize_all_variables().run()
sess.run(tf.initialize_all_variables())



#defining the loss function
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))


#defining the optimizeation algorithm

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)


#running the algorithm e times:
for r in range(1000):
	for i in range(1000):
		batch = mnist.train.next_batch(100)
		train_step.run(feed_dict={x:batch[0], y_:batch[1]})

		#getting the accuracy for the training set

	correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
	print(sess.run(accuracy, feed_dict={x: mnist.test.images,
                                      y_: mnist.test.labels}))









