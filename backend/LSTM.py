from tensorflow.contrib.rnn import LSTMCell, LSTMStateTuple
import tensorflow as tf
import matplotlib.pyplot as plt2
import input_data
import numpy as np
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from constants import batch_size, epochs, dropout, variables_device,\
					 sequence_length, learning_rate, display_steps,\
					 prediction_length, processing_device
from funcs import defineVariables, preActivation, activation


company_str = input("Enter company name for training:  ")

while not os.path.exists("../csv-data/gainers/"+ company_str + ".NS.csv"):
	print "Company not found"
	company_str = input("Enter company name for training:  ")


company = input_data.load_data(company = company_str)

# placeholders
seq_input = tf.placeholder(tf.float32,
							shape = (None, sequence_length, 4),
							name="input_to_lstm")

seq_output = tf.placeholder(tf.float32, 
							shape = (None, 4*prediction_length), 
							name= "output_of_model")

with tf.device(variables_device):
	# weights
	fc_weights = {
		'wfc1' : defineVariables([120, 80],"wfc1"),
		'wfc2' : defineVariables([80, 64], "wfc2"),
		'out' : defineVariables([64, 40], "wout")
	}
	attention_weights = {
		'lstm1': defineVariables([1, 30, 2], "weights_lstm1")
	}

	# biases
	fc_biases = {
		'bfc1' : defineVariables([80], 'bfc1'),
		'bfc2' : defineVariables([64], 'bfc2'),
		'out' : defineVariables([40], 'bout')
	}
	attention_biases = {
		'lstm1' : defineVariables([2], "biases_lstm1")
	}


# model for prediction
with tf.variable_scope("lstm_layer1") as scope:
	# bidirectional lstm layer
	fw_lstm = LSTMCell(sequence_length)
	bw_lstm = LSTMCell(sequence_length)
	(fw_output, bw_output),(fw_finalstate, bw_finalstate) = \
		tf.nn.bidirectional_dynamic_rnn(cell_fw = fw_lstm,
										cell_bw = bw_lstm,
										inputs = seq_input,
										dtype = tf.float32)
	lstm_finalstates = tf.concat((tf.concat(\
						(fw_finalstate.h, bw_finalstate.h),\
							1), tf.concat((fw_finalstate.c,\
							bw_finalstate.c), 1)),1)

	# useful for attention modelling
	lstm_outputs = tf.concat((fw_output, bw_output), 1)

with tf.variable_scope("attention") as scope:
	attention_weight = tf.tile(attention_weights['lstm1'],
								[batch_size, 1, 1])

	# attention to lstm layer1
	attention = preActivation(lstm_outputs, 
							attention_weight,
							attention_biases['lstm1'])
	
	attention_out = activation(attention)

	# reshape data for decoding the information
	attention_reshape = tf.reshape(attention_out, (batch_size, 120))

with tf.variable_scope("fully_connected") as scope:
	fc1 = preActivation(attention_reshape, 
						fc_weights['wfc1'],
						fc_biases['bfc1'])
	fc1_out = activation(fc1)

	fc2 = preActivation(fc1_out, 
						fc_weights['wfc2'], 
						fc_biases['bfc2'])
	fc2_out = activation(fc2)

	out = preActivation(fc2_out,
						fc_weights['out'],
						fc_biases['out'])
	out = activation(out)

start_time = time.time()
# use MSE for cost function
cost = tf.losses.mean_squared_error(out, seq_output)

# regularization term L2 normalization for loss calculation
# conc
regularizer = tf.nn.l2_loss(fc_weights['wfc1']) +\
			  tf.nn.l2_loss(fc_weights['wfc2']) +\
			  tf.nn.l2_loss(fc_weights['out'])
reg_loss = tf.reduce_mean(cost + 1e-2 * regularizer)

# optimizer function using RMSProp/ Adam optimizer
optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(reg_loss)

print "Compilation time:  {}sec".format(time.time() - start_time)
# MSE error matrix 
# mse, update = tf.metrics.mean_squared_error(seq_output,
# 											out, 
# 											name="prediction_error")
# TODO:

init = tf.global_variables_initializer()
with tf.device(processing_device):
	with tf.Session() as sess:
		sess.run(init)
		train_start = time.time()
		step = 1
		while company.train.epochs_completed <= epochs:
			step += 1
			company_data, company_labels = company.train.next_batch()
			output_data = np.reshape(company_labels, (batch_size, 4*prediction_length))

			sess.run(optimizer, feed_dict={seq_input: company_data, seq_output: output_data})

			loss = sess.run(cost, feed_dict={seq_input: company_data, seq_output: output_data})

			if step % display_steps == 0:
				print "Epochs completed: {}".format(company.train.epochs_completed) +\
				 				"  loss: {}".format(loss) + "  step: {}".format(step)
				 			

		print "Optimization Completed. Training time:  {}sec".format(time.time() - train_start)	

		test_data, test_labels = company.test.next_batch()
		predictions = sess.run(out, feed_dict={seq_input: test_data})
		predictions = np.reshape(predictions, (25, 10, 4))
		labels, pred = [], []
		for data, label, prediction in zip(test_data, test_labels, predictions):
			labels.append(np.concatenate((data,label), 0).tolist())
			pred.append(np.concatenate((data, prediction),0).tolist()) 	

		final_data, final_label = [], []
		for d, l in zip(labels, pred):
			final_data.append(d[0])
			final_label.append(l[0])

		fdata = final_data[:-1] + pred[len(pred) - 1:][0]
		flabels = final_label[:-1] + labels[len(labels) - 1:][0]
		
		fdata = np.array(fdata)
		flabels = np.array(flabels)

		plt2.plot(fdata.T[0], color='red', label='prediction')
		plt2.plot(flabels.T[0], color='blue', label='actual')
		plt2.legend(loc='upper left')
		plt2.show()