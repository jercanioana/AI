# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 10:51:09 2020

@author: ioana
"""
import random
import copy
from math import exp, sin
import matplotlib as mpl
def linearFct(x):
    return -1/18*x

def dlinearFct(x):
    return -1/18


def identical(x):
    return x

class Neuron:
    def __init__(self, noOfInputs, activationFct):
        self.noOfInputs = noOfInputs
        self.activationFct = activationFct
        self.weights = [random.random() for i in range(self.noOfInputs)]
        self.output = 0
    
    def setWeights(self, newWeights):
        self.weights = newWeights
        
    def fireNeuron(self, inputs):
        
        inp = sum([x*y for x,y in zip(inputs, self.weights)])
        self.output = self.activationFct(inp)
        return self.output
    
    def __str__(self):
        return "Weights: " + str(self.weights)
    
class Layer:
    def __init__(self, noOfInputs, activationFct, noOfNeurons):
        self.noOfNeurons = noOfNeurons
        self.neurons = [Neuron(noOfInputs, activationFct) for neuron in range(self.noOfNeurons)]
        
    def forwardFct(self, inputs):
        for neuron in self.neurons:
            
            neuron.fireNeuron(inputs)
        return([neuron.output for neuron in self.neurons])
    
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
        
        newNetwork = Network(self.structure, self.activationFct, self.derivative, self.bias)
        noOfNeuronsForLastLayer = self.structure[-1]
        for i in range(noOfNeuronsForLastLayer):
            delta.append(error[i]*self.derivative(self.layers[-1].neurons[i].output))
            for r in range(self.structure[self.noOfLayers-2]):
                newNetwork.layers[-1].neurons[i].weights[r] = self.layers[-1].neurons[i].weights[r] + learningRate*delta[i]*self.layers[self.noOfLayers-2].neurons[r].output
                
        for currentLayer in range(self.noOfLayers-2, 0, -1):
            currentDelta = []
            for i in range(self.structure[currentLayer]):
                currentDelta.append(self.derivative(self.layers[currentLayer].neurons[i].output)*sum([self.layers[currentLayer+1].neurons[j].weights[i]*delta[j] for j in range(self.structure[currentLayer+1])]))
            delta = currentDelta[:]
            for i in range(self.structure[currentLayer]):
                for r in range(self.structure[currentLayer-1]):
                    newNetwork.layers[currentLayer].neurons[i].weights[r] = self.layers[currentLayer].neurons[i].weights[r] + learningRate * delta[i] * self.layers[currentLayer-1].neurons[r].output
        self.layers = copy.deepcopy(newNetwork.layers)
        
    def computeLoss(self, inputs, realoutput):
        loss = []
        output = self.feedForward(inputs)
        for i in range(len(realoutput)):
            loss.append(inputs[i] - output[i])
        return loss[:]
    
    def __str__(self):
        s = ''
        for i in range(self.noOfLayers):
            print(self.noOfLayers)
            s += ' layer:  '+str(i)+' :'+str(self.layers[i])
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
            self.__network = Network([5,6,1], linearFct, dlinearFct)
        
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
        
        print(str(self.__network))
        mpl.pyplot.plot(iterations, errors)
        mpl.pyplot.xlabel('Iterations')
        mpl.pyplot.ylabel('Error')
        mpl.pyplot.show()
        

c = Controller("data2.txt")
c.trainNetwork()
