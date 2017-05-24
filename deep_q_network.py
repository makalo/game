#!/usr/bin/env python
from __future__ import print_function

import tensorflow as tf
import cv2
import sys
sys.path.append("game/")

import t2
import random

import numpy as np


GAME = 'snake' # the name of the game being played for log files
ACTIONS = 4 # number of valid actions
EXPLORE = 2000000. # frames over which to anneal epsilon
FRAME_PER_ACTION = 1
INITIAL_EPSILON = 0.05
FINAL_EPSILON = 0.05

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.01)
    return tf.Variable(initial)
def bias_variable(shape):
    initial = tf.constant(0.01, shape = shape)
    return tf.Variable(initial)
def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides = [1, stride, stride, 1], padding = "SAME")
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = "SAME")
class createNetwork():
    def __init__(self):
        self.W_conv1 = weight_variable([8, 8, 4, 32])
        self.b_conv1 = bias_variable([32])

        self.W_conv2 = weight_variable([4, 4, 32, 64])
        self.b_conv2 = bias_variable([64])

        self.W_conv3 = weight_variable([3, 3, 64, 64])
        self.b_conv3 = bias_variable([64])

        self.W_fc1 = weight_variable([1600, 512])
        self.b_fc1 = bias_variable([512])

        self.W_fc2 = weight_variable([512, ACTIONS])
        self.b_fc2 = bias_variable([ACTIONS])

        # input layer
        self.s = tf.placeholder("float", [None, 80, 80, 4])

        # hidden layers
        self.h_conv1 = tf.nn.relu(conv2d(self.s, self.W_conv1, 4) + self.b_conv1)
        self.h_pool1 = max_pool_2x2(self.h_conv1)

        self.h_conv2 = tf.nn.relu(conv2d(self.h_pool1, self.W_conv2, 2) + self.b_conv2)
        #h_pool2 = max_pool_2x2(h_conv2)

        self.h_conv3 = tf.nn.relu(conv2d(self.h_conv2, self.W_conv3, 1) + self.b_conv3)
        #h_pool3 = max_pool_2x2(h_conv3)

        #h_pool3_flat = tf.reshape(h_pool3, [-1, 256])
        self.h_conv3_flat = tf.reshape(self.h_conv3, [-1, 1600])

        self.h_fc1 = tf.nn.relu(tf.matmul(self.h_conv3_flat, self.W_fc1) + self.b_fc1)

        # readout layer
        self.readout = tf.matmul(self.h_fc1, self.W_fc2) + self.b_fc2
        self.predict = tf.argmax(self.readout, 1)
        self.a = tf.placeholder("float", [None, ACTIONS])
        self.y = tf.placeholder("float", [None])
        self.readout_action = tf.reduce_sum(tf.multiply(self.readout, self.a), reduction_indices=1)
        self.cost = tf.reduce_mean(tf.square(self.y - self.readout_action))
        self.train_step = tf.train.AdamOptimizer(1e-6).minimize(self.cost)
   
def trainNetwork(current_q,sess):
    
    game_state = t2.game()
    
    do_nothing = np.zeros(ACTIONS)
   
    do_nothing[random.randrange(ACTIONS)] = 1
    
    s_t,terminal= game_state.frame_step(do_nothing)
    s_t = cv2.cvtColor(cv2.resize(s_t, (80, 80)), cv2.COLOR_BGR2GRAY)
    _, s_t = cv2.threshold(s_t,1,255,cv2.THRESH_BINARY)
    s_1 = np.stack((s_t, s_t, s_t, s_t), axis=2)

    sess.run(tf.global_variables_initializer())
    checkpoint = tf.train.get_checkpoint_state("saved_networks")
    saver = tf.train.Saver()
    if checkpoint and checkpoint.model_checkpoint_path:
        saver.restore(sess, checkpoint.model_checkpoint_path)
        print("Successfully loaded:", checkpoint.model_checkpoint_path)
    else:
        print("Could not find old network weights")
    epsilon = INITIAL_EPSILON
    while (True):
        # choose an action epsilon greedily
        readout_t = current_q.readout.eval(feed_dict={current_q.s : [s_1]})[0]
        a_t = np.zeros([ACTIONS])
        action_index = 0
 
        if random.random() <= epsilon:
           
            action_index = random.randrange(ACTIONS)
            a_t[random.randrange(ACTIONS)] = 1
        else:
            action_index = np.argmax(readout_t)
            a_t[action_index] = 1
        if terminal:
            a_t = np.zeros([ACTIONS])
            a_t[random.randrange(ACTIONS)] = 1
      
        if epsilon > FINAL_EPSILON:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE
        
        # run the selected action and observe next state and reward
        s_t2,terminal= game_state.frame_step(a_t)
        s_t2 = cv2.cvtColor(cv2.resize(s_t2, (80, 80)), cv2.COLOR_BGR2GRAY)
        ret, s_t2 = cv2.threshold(s_t2, 1, 255, cv2.THRESH_BINARY)
        s_t2 = np.reshape(s_t2, (80, 80, 1))
        s_2 = np.append(s_t2, s_1[:, :, :3], axis=2)

        s_1=s_2
def playGame():
    
    current_q= createNetwork()
    sess = tf.InteractiveSession()
    trainNetwork(current_q,sess)

def main():
    playGame()

if __name__ == "__main__":
    main()
