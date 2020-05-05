# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 14:04:56 2020

@author: ioana
"""
import numpy as np
import random

class Node:
    def __init__(self, info):

        self.__next = []
        self.__info = info
        self.__class = None
        self.__separatingAttribute = None
    
    def getInfo(self):
        return self.__info
    
    def getNext(self):
        return self.__next
        
    def setLabel(self, label):
        self.__class = label
    
    def getLabel(self):
        return self.__class
    
    def setNext(self, nxt):
        self.__next.append(nxt)
    
    def getSeparationAttr(self):
        return self.__separatingAttribute
    
    def setSeparationAttr(self, attr):
        self.__separatingAttribute = attr
        
    def isRoot(self):
        return self.getLabel() != None

        
class Controller:
    def __init__(self, filePath):
        self.__filePath = filePath
        self.__trainData = []
        self.__testData = []
        self.__predictions = 0
        self.loadData()
        self.__total = len(self.__testData)
        
    def loadData(self):
        counterSeparator = 1
        f = open(self.__filePath, "r")
        for line in f:
            line = line[:-1]
            DS = line.split(",")
            if counterSeparator <= 550:
                self.__trainData.append(DS)
            else:
                self.__testData.append(DS)
            counterSeparator += 1
        
        f.close()
        
    
    
    def check(self, data_sample, node):
        if node.isRoot():
            return node.getLabel() == data_sample[0]
        nxt = node.getNext()
        i = 0
        while i < len(nxt) != 0:
            n = nxt[i]
            i += 1
            info = n.getInfo()
            if n.getLabel() != None:
                return self.check(data_sample, n)
            elif info[0][node.getSeparationAttr()] == data_sample[node.getSeparationAttr()]:
                return self.check(data_sample, n)
            
    def checkTest(self, nodes):
       
        for data in self.__testData:
            if self.check(data, nodes) == True:
                self.__predictions += 1

    
    def accuracy(self, nodes):
        
        self.checkTest(nodes)
        return float(self.__predictions/self.__total)*100
        
    def checkClass(self,data):
        clasa = data[0][0]
        for dat in data:
            if dat[0] != clasa:
                return False, None
        return True, clasa
    
    def giniIndex(self, index, data):
        numberForRgreater = 0
        numberForLgreater = 0
        numberForBgreater = 0
        numberForRLower = 0
        numberForLLower = 0
        numberForBLower = 0
        numberGreater = 0
        numberLower = 0
        values = []
        for d in data:
            values.append(d[index])
            
        if(len(values) > 1):
            r = np.random.randint(0, len(values)-1)
        else:
            r = 0
        randomValue = int(values[r])
       
        for d in data:
            if int(d[index]) <= randomValue and d[0] == "L":
                
                numberForLLower += 1
                numberLower += 1
            elif int(d[index]) <= randomValue and d[0] == "B":
                
                numberForBLower += 1
                numberLower += 1
            elif int(d[index]) <= randomValue and d[0] == "R":
               
                numberForRLower += 1
                numberLower += 1
            elif int(d[index]) > randomValue and d[0] == "L":
                
                numberForLgreater += 1
                numberGreater += 1
            elif int(d[index]) > randomValue and d[0] == "B":
                
                numberForBgreater += 1
                numberGreater += 1
            elif int(d[index]) > randomValue and d[0] == "R":
                
                numberForRgreater += 1
                numberGreater += 1
        if numberGreater == 0:
            numberGreater = 0.01
        value1 = 1 - (float(numberForLLower / numberLower)) ** 2  - (float(numberForRLower / numberLower)) ** 2 - (float(numberForBLower / numberLower)) ** 2
        value2 = 1 - (float(numberForLgreater / numberGreater)) ** 2  - (float(numberForRgreater / numberGreater)) ** 2 - (float(numberForBgreater / numberGreater)) ** 2
        gini = (float(numberLower / len(data))) * value1 + (float(numberGreater / len(data))) *  value2
        
        return gini
        
    def attributeSelection(self, data, attributes):
        attr = []
        for a in attributes:
            attr.append((a, self.giniIndex(a, data)))
        attr.sort(key=lambda x:x[1])
        return attr[0][0]
    
    def majorityClass(self, data):
        
        classes = []
        
        counterL = 0
        counterB = 0
        counterR = 0
        for d in data:
            if d[0] == "L":
                counterL += 1
            elif d[0] == "B":
                counterB += 1
            elif d[0] == "R":
                counterR += 1
        
        classes.append(("L", counterL))
        classes.append(("R", counterR))
        classes.append(("B",counterB))
        classes.sort(key=lambda x:x[1])
        
        c,n = classes[2]
        
        return c
    
        
            
    def getData(self):
        return self.__trainData
        
    def generate(self,data, attributes):
        node = Node(data)
        condition, clasa = self.checkClass(data)
        
        if condition == True:
            node.setLabel(clasa)
            return node
        
        else:
            if len(attributes) == 0:
                c = self.majorityClass(data)
               
                node.setLabel(c)
                return node
            else:
                separationAttr = self.attributeSelection(data, attributes)
                attributes.remove(separationAttr)
                node.setSeparationAttr(separationAttr)
                
                for i in range(1,6):
                    newData = []
                    for d in data:
                        if int(d[separationAttr]) == i:
                            newData.append(d)
                    if len(newData) == 0:
                        
                        newNode = Node(newData)
                        cl = self.majorityClass(data)
                        newNode.setLabel(cl)
                        node.setNext(newNode)
                    else:
                        node.setNext(self.generate(newData,attributes))
                return node
                        
            
        
    
class UI:
    def run_menu(self):
        while True:
            print("1. Run Algorithm")
            print("0. Exit")
            opt = int(input())
            if opt == 1:
                ctl = Controller("data.txt")
                attributesidx = [1,2,3,4]
                nodes = ctl.generate(ctl.getData(), attributesidx)
                print("Accuracy: " + str(ctl.accuracy(nodes)) + "%")
            elif opt == 0:
                break
        

ui = UI()
ui.run_menu()
