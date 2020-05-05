# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:53:47 2020

@author: ioana
"""
import numpy as np
import random
import matplotlib as mpl
#the activation function:
def sigmoid(x):
    return 1.0/(1+ np.exp(-x))

#the derivate of te activation function
def sigmoid_derivative(x):
    return x * (1.0 - x)

class NeuralNetwork:
    def __init__(self, x, y, hidden):
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1],hidden)
        self.weights2 = np.random.rand(hidden,1)
        self.y = y
        self.output = np.zeros(y.shape)
        
    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.output = sigmoid(np.dot(self.layer1, self.weights2))
        
    def backprop(self,l_rate):
    # application of the chain rule to find derivative of the    
    #loss function with respect to weights2 and weights1
           d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) *
                            sigmoid_derivative(self.output)))
           
           d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y -
                            self.output) * sigmoid_derivative(self.output),
                            self.weights2.T) *
                             sigmoid_derivative(self.layer1)))
           # update the weights with the derivative (slope) of the loss function
           
           self.weights1 += l_rate * d_weights1
           self.weights2 += l_rate * d_weights2
           self.loss.append(sum((self.y - self.output)**2))

if __name__ == "__main__":
    #X the array of inputs, y the array of outputs, 4 pairs in total 
    x = np.array([])
    y = np.array([])
    f = open("data2.txt", "r")
    for line in f:
        x_i = np.array([])
        line = line[:-1]
        DS = line.split(" ")
        if(len(DS) > 1):
            for i in range(0, len(DS)-1):
                np.append(x_i,[DS[i]])
                print(x_i)
            np.append(y,DS[5])
            np.append(x,x_i)
    f.close()
    print(x)
    nn = NeuralNetwork(x,y,2)
    
    nn.loss=[]
    iterations =[]
    for i in range(4000):
        nn.feedforward()
        nn.backprop(1)
        iterations.append(i)

    print(nn.output)
    mpl.pyplot.plot(iterations, nn.loss, label='loss value vs iteration')
    mpl.pyplot.xlabel('Iterations')
    mpl.pyplot.ylabel('loss function')
    mpl.pyplot.legend()
    mpl.pyplot.show()