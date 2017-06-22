import tensorflow as tf
import sys
import time
import os
from constants import batch_size, epochs, dropout, variables_device,\
					 sequence_length, learning_rate, display_steps,\
					 prediction_length, processing_device, IS_RESTORE_BASED
from MLP import take_input, create_directory, define_placeholders,\
				load_company_data, print_status, declare_variables,\
				model, model_compilation, run_model, p_values

COMPANY_LIST = ['VEDL', 'BPCL', 'RELIANCE', 'HINDALCO', 'YESBANK']

def network(companyname):
	create_directory(companyname)
	seq_input, seq_output, keep_prob = define_placeholders(sequence_length,
														prediction_length)
	company = load_company_data(companyname)
	weights, biases = declare_variables(sequence_length, 
										prediction_length, 
										variables_device,
										companyname)
	model_output = model(seq_input, weights, biases, keep_prob, companyname)
	print_status(learning_rate, batch_size, epochs, companyname)
	saver, optimizer, cost = model_compilation(model_output, 
										 seq_output, 
										 learning_rate, 
										 weights)
	total_error, unexplained_error, R_squared, R, MAPE, RMSE = p_values(seq_output, model_output)
	init = tf.global_variables_initializer()
	run_model(init, model_output, saver, IS_RESTORE_BASED, companyname,\
			 company, epochs, seq_input, seq_output,\
			 keep_prob, dropout, optimizer, cost,\
			 batch_size, prediction_length, sequence_length, processing_device,\
			 display_steps, weights, biases, total_error, unexplained_error, R_squared, R, MAPE, RMSE)



trainstart = time.time()
for company in COMPANY_LIST:
	print "CURRENT COMPANY: {}".format(company)
	network(company)

print "TOTAL TRAINING TIME: {}".format(time.time() - trainstart)