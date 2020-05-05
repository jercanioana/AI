# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 10:51:09 2020

@author: ioana
"""
import random
import copy
from math import exp, sin
import matplotlib as mpl
def identical(x):
    return x

def dIdentical(x):
    return 1

def ReLU(x):
    return max(0, x)

def dReLU(x):
    if x > 0:
        return 1
    else:
        return 0
    
def threshold(x):
    if x > 0.2:
        return 1
    return 0

def dThreshold(x):
    # is just to have some function when we train the network
    return 1

def sigmoid(x):
    return (1.0  /(1.0 + exp(-x)))

def dSigmoid(x):
    return x * (1.0 - x)

def linearFct(x):
    return -x+5

def dlinearFct(x):
    return -1


def identical(x):
    return x

class Neuron:
    def __init__(self, noOfInputs, activationFct):
        self.noOfInputs = noOfInputs
        self.activationFct = activationFct
        self.weights = [random.random() for i in range(self.noOfInputs)]
        self.outputs = 0
    
    def setWeights(self, newWeights):
        self.weights = newWeights
        
    def fireNeuron(self, inputs):
        
        inp = sum([x*y for x,y in zip(inputs, self.weights)])
        self.output = self.activationFct(inp)
        return self.output
    
    def __str__(self):
        return str(self.weights)
    
class Layer:
    def __init__(self, noOfInputs, activationFct, noOfNeurons):
        self.noOfNeurons = noOfNeurons
        self.neurons = [Neuron(noOfInputs, activationFct) for neuron in range(self.noOfNeurons)]
        
    def forwardFct(self, inputs):
        for neuron in self.neurons:
            
            neuron.fireNeuron(inputs)
        return([neuron.outputs for neuron in self.neurons])
    
    def __str__(self):
        s = ''
        for i in range(self.noOfNeurons):
            s += ' n '+str(i)+' '+str(self.neurons[i])+'\n'
        return s
    
class FirstLayer(Layer):
    def __init__(self, noOfNeurons, bias = False):
        if bias:
            noOfNeurons = noOfNeurons + 1
            
        Layer.__init__(self, 1, identical, noOfNeurons)
        for x in self.neurons:
            x.setWeights([1])
    
    def forwardFct(self, inputs):
        for i in range(len(self.neurons)):
                self.neurons[i].fireNeuron(inputs)
        return ([neuron.output for neuron in self.neurons])
    
class Network:
    def __init__(self, structure, activationFct, derivative, bias = False):
        self.activationFct = activationFct
        self.derivative = derivative
        self.bias = bias
        self.structure = structure
        self.noOfLayers = len(self.structure)
        self.layers = [FirstLayer(self.structure[0], bias)]
        for i in range(1, len(self.structure)):
           self.layers = self.layers + [Layer(self.structure[i-1], activationFct, self.structure[i])]
        
    def feedForward(self, inputs):
        self.signal= inputs[:]
        if self.bias:
            self.signal.append(1)
        for layer in self.layers:
            self.signal = layer.forwardFct(self.signal)
        return self.signal
    
    def backPropag(self, loss, learningRate):
        error = loss[:]
        delta = []
        currentLayer = self.noOfLayers-1
        newNetwork = Network(self.structure, self.activationFct, self.derivative, self.bias)
        
        for i in range(self.structure[-1]):
            delta.append(error[i]*self.derivative(self.layers[-1].neurons[i].output))
            for r in range(self.structure[currentLayer-1]):
                newNetwork.layers[-1].neurons[i].weights[r] = self.layers[-1].neurons[i].weights[r] + learningRate*delta[i]*self.layers[currentLayer-1].neurons[r].output
                
        for currentLayer in range(self.noOfLayers-2, 0, -1):
            currentDelta = []
            for i in range(self.structure[currentLayer]):
                currentDelta.append(self.derivative(self.layers[currentLayer].neurons[i].output)*sum([self.layers[currentLayer+1].neurons[j].weights[i]*delta[j] for j in range(self.structure[currentLayer+1])]))
            delta = currentDelta[:]
            for i in range(self.structure[currentLayer]):
                for r in range(self.structure[currentLayer-1]):
                    newNetwork.layers[currentLayer].neurons[i].weights[r] = self.layers[currentLayer].neurons[i].weights[r] + learningRate * delta[i] * self.layers[currentLayer-1].neurons[r].output
        self.layers = copy.deepcopy(newNetwork.layers)
        
    def computeLoss(self, x, y):
        loss = []
        output = self.feedForward(x)
        for i in range(len(y)):
            loss.append(x[i] - output[i])
        return loss[:]
    
    def __str__(self):
        s = ''
        for i in range(self.noOfLayers):
            s += ' l '+str(i)+' :'+str(self.layers[i])
        return s
    
class Controller:
    
    def __init__(self, file):
        self.__file = file
        self.__network = None
        self.__input = []
        self.__output = []
        self.loadData()
        
    def loadData(self):
        
        
        f = open(self.__file, "r")
        for line in f:
            x_i = []
            line = line[:-1]
            DS = line.split(" ")
        
            if(len(DS) > 1):
                for i in range(0, len(DS)-1):
                    
                    x_i.append(float(DS[i]))
                self.__output.append([float(DS[5])])
                self.__input.append(x_i)
            self.__network = Network([5,4,1], ReLU, dReLU)
        
        f.close()
        
    def trainNetwork(self):
        errors = []
        iterations = []
        
        for i in range(100):
            iterations.append(i)
            e = []
            for j in range(len(self.__input)):
                e.append(self.__network.computeLoss(self.__input[j],self.__output[j])[0])
                self.__network.backPropag(self.__network.computeLoss(self.__input[j],self.__output[j]), 0.01)
            errors.append(sum([x**2 for x in e]))
        for j in range(len(self.__input)):
            self.__network.feedForward(self.__input[j])
            print(self.__input[j], self.__output[j], self.__network.feedForward(self.__input[j]))
        #print(str(self.__network))
        mpl.pyplot.plot(iterations, errors, label='loss value vs iteration')
        mpl.pyplot.xlabel('Iterations')
        mpl.pyplot.ylabel('loss function')
        mpl.pyplot.legend()
        mpl.pyplot.show()
        
c = Controller("data2.txt")
c.trainNetwork()
