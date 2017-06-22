import tensorflow as tf
import numpy as np

def defineVariables(shape, name): 
    initializer = tf.contrib.layers.variance_scaling_initializer()
    return tf.get_variable(name, shape, initializer=initializer, dtype=tf.float32)

def preActivation(x, w, b):
    return tf.add(tf.matmul(x, w), b)

def activation(x):
    return tf.nn.sigmoid(x)

def save(list2save, directory):
	np.save(directory, list2save)
	pass