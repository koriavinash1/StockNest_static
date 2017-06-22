import tensorflow as tf
import sys
import os
from constants import batch_size, epochs, dropout, variables_device,\
					 sequence_length, learning_rate, display_steps,\
					 prediction_length, processing_device, IS_RESTORE_BASED
from test import define_placeholders,\
				load_company_data,load_variables,\
				model, model_compilation, run_model

COMPANY_LIST = ['VEDL', 'BPCL', 'RELIANCE', 'HINDALCO', 'YESBANK']

def network(companyname):
	seq_input, seq_output, keep_prob = define_placeholders(sequence_length,
														prediction_length)
	company = load_company_data(companyname)
	weights, biases = load_variables( variables_device,
										companyname)
	model_output = model(seq_input, weights, biases, keep_prob, companyname)
	cost = model_compilation(model_output, seq_output)
	init = tf.global_variables_initializer()
	run_model(init, model_output, companyname,\
			 company, seq_input, seq_output,\
			 keep_prob, dropout, cost, batch_size,\
			 prediction_length, sequence_length, processing_device)



for company in COMPANY_LIST:
	print "CURRENT COMPANY: {}".format(company)
	network(company)