# simple graph just using MLP for prediction
import tensorflow as tf
import matplotlib.pyplot as plt2
import input_data
import numpy as np
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from funcs import preActivation, save

from input_data import data_denormalization
# placeholders
def define_placeholders(sequence_length, prediction_length):
	seq_input = tf.placeholder(tf.float32,
								shape = (None, sequence_length),
								name="input_to_model")

	seq_output = tf.placeholder(tf.float32, 
								shape = (None, prediction_length), 
								name= "output_of_model")

	keep_prob = tf.placeholder(tf.float32)
	return seq_input, seq_output, keep_prob

def load_company_data(company_str):
	company = input_data.load_data(company = company_str)
	return company

def define_variable(value, name): 
    return tf.Variable(value, name = name)

def load_variables(variables_device, company_str):
	with tf.device(variables_device):
		weights = {
			'layer1' : define_variable(np.load("../modeldata/"+company_str+"/weights/layer1.npy"), company_str+'wc1'),
			'layer2' : define_variable(np.load("../modeldata/"+company_str+"/weights/layer2.npy"), company_str+'wc2')
		}
		biases = {
			'layer1': define_variable(np.load("../modeldata/"+company_str+"/biases/layer1.npy"), company_str+'bc1'),
			'layer2': define_variable(np.load("../modeldata/"+company_str+"/biases/layer2.npy"), company_str+'bc2')
		}
	return weights, biases

def model(seq_input, weights, biases, keep_prob, company_str):
	with tf.variable_scope(company_str+'MLP_layer1') as scope:
		pre_activation = preActivation(seq_input, weights['layer1'], biases['layer1'])
		activation = tf.nn.sigmoid(pre_activation)
		dropout_layer = tf.nn.dropout(activation, keep_prob, name="dropout2")

	with tf.variable_scope(company_str+'MLP_layer2') as scope:
		pre_activation = preActivation(dropout_layer, weights['layer2'], biases['layer2'])
		output = pre_activation
	return output

def model_compilation(output, seq_output):
	start_time = time.time()
	# use MSE for cost function
	cost = tf.losses.mean_squared_error(output, seq_output)
	print "Compilation time:  {}sec".format(time.time() - start_time)

	return cost

def run_model(init, output, company_str, company, seq_input, seq_output, keep_prob, dropout, cost, batch_size, prediction_length, sequence_length, processing_device):
	merged = tf.summary.merge_all()
	with tf.device(processing_device):
		with tf.Session() as sess:
			sess.run(init)
			company_data = company.test.data.T[1].T[-1:]
			# output_data = company.test.labels.T[1].T[-1:]

			codate = company.test.data.T[0].T[-1:]
			# labdate = company.test.labels.T[0].T[-1:]
			
			# output_data = np.reshape(output_data, (1, prediction_length))
			company_data = np.reshape(company_data, (1, sequence_length))

			# predictions, loss = sess.run([output, cost], feed_dict={seq_input: company_data, seq_output: output_data, keep_prob: dropout})
			predictions = sess.run(output, feed_dict={seq_input: company_data, keep_prob: dropout})
			predictions = np.reshape(predictions, (1, prediction_length))

			# print "loss: {}".format(loss)
	 
	        # labels, pred, datetime= [], [], []
	        # for data, label, prediction, adt, ldt in zip(company_data, output_data, predictions, codate, labdate):
	        # 	labels.append(np.concatenate((data,label), 0).tolist())
	        # 	pred.append(np.concatenate((data, prediction),0).tolist())
	        # 	datetime.append(np.concatenate((adt, ldt), 0).tolist())

	        # error = 0.05
	        # pred, labels = data_denormalization(pred[0], labels[0], company_str)
	        # resultfile = open("../resultfile.txt", "a")
	        # if pred[len(pred) - 2] > (pred[len(pred) - 1] + error):
	        # 	res_str =  "CLOSING PRICE WILL GO UP FOR "+ company_str +" >> BUY MORE SHARE..."
	        # else:
	        # 	res_str = "CLOSING PRICE WILL GO Down FOR "+ company_str +" >> SELL MORE SHARE..."

	        # resultfile.write(res_str)
	        # resultfile.write("\n")

	        pred, datetime= [], []
	        for data, prediction, adt in zip(company_data, predictions, codate):
	        	pred.append(np.concatenate((data, prediction),0).tolist())
	        	datetime.append(np.array(adt).tolist())
	        error = 50
	        pred = data_denormalization(pred[0], company_str)
	        resultfile = open("../resultfile.txt", "a")
	        if pred[len(pred) - 2] > (pred[len(pred) - 1] + error):
	        	res_str =  "CLOSING PRICE WILL GO UP FOR "+ company_str +" >> BUY MORE SHARE..."
	        else:
	        	res_str = "CLOSING PRICE WILL GO Down FOR "+ company_str +" >> SELL MORE SHARE..."

	        resultfile.write(res_str)
	        resultfile.write("\n")

	        datafile = open("../graphdata/"+company_str+"_data.js", "w")
	        labelfile = open("../graphdata/"+company_str+"_label.js", "w")
	        datafile.write("var " +company_str+"_CLOSING_PRICE_DATA = [ 0")
	        labelfile.write("var " +company_str+"_CLOSING_PRICE_LABEL = [ 0")
	        for dat in pred:
	        	datafile.write(", '")
	        	datafile.write(str(dat))
	        	datafile.write("'")
	        
	        for lab in datetime[0]:
	        	labelfile.write(", '")
	        	labelfile.write(str(lab))
	        	labelfile.write("'")

	        datafile.write(" ];")
	        labelfile.write(", 'Day +1', 'Day +2'];")

	        datafile.close()
	        labelfile.close()