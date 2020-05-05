# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 10:41:47 2020

@author: ioana
"""

class Problem:
    def __init__(self, x, y):
        self.__x = x
        self.__x_means = []
        self.__y_mean = 0.0

        self.__y = y
        self.calculateMeanX()
        self.calculateMeanY()

        
    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y
        
    def calculateMeanX(self):
        num = len(self.__x)
        i = 0
        while i < 5:
            sumX = 0.0
            meanX = 0.0
            for data in self.__x:
                sumX += float(data[i])
                
            meanX = sumX/num
            self.__x_means.append(meanX)
            i += 1
                
    def calculateMeanY(self):
        num = len(self.__y)
        
        sumY = 0.0
        for data in self.__y:
            sumY += float(data)
            
        self.__y_mean = sumY / num
        
                
    def calculateCoefficient(self):
        beta = []

        s = 0.0
        
    
        for k in range(0,5):
            meanX = self.__x_means[k]
            s1 = 0.0
            s2 = 0.0
            for i in range(len(self.__x)-1):
                s1 += float(((float (self.__x[i][k]) - meanX) ** 2))
                s2 += (float(self.__x[i][k]) - meanX) * (float(self.__y[i]) - self.__y_mean)
                
            betai = float(s2/s1)
            beta.append(betai)
            s += float(meanX * betai)
        
            
        betai = self.__y_mean - s
        beta.append(betai)
        return beta
    
    def findF(self, x):
        coef = self.calculateCoefficient()
        xi = 0.0
        j = 0
        while j < 5:
            xi += float(float(x[j]) * float(coef[j]))
            j += 1
        xi += coef[5]
        return xi
            
            
    def Loss(self):
        loss = 0.0
        fct = 0.0
        for i in range(len(self.__x)-1):
            fct += self.findF(self.__x[i])
            loss += float(float(self.__y[i]) - self.findF(self.__x[i])) ** 2
        
        return loss, fct
            
        
class Controller:
    def __init__(self, file):
        self.__file = file
        self.__problem = None
        self.loadData()
        
    def loadData(self):
        x = []
        y = []
        f = open(self.__file, "r")
        for line in f:
            x_i = []
            line = line[:-1]
            DS = line.split(" ")
        
            if(len(DS) > 1):
                for i in range(0, len(DS)-1):
                    
                    x_i.append(DS[i])
                y.append(DS[5])
                x.append(x_i)
            
        self.__problem = Problem(x, y)
        f.close()
        
   
        
            
    def runAlgorithm(self):
        coef = self.__problem.calculateCoefficient()
       
        return self.__problem.Loss()
                
            
        
class UI:
    def __init__(self, controller):
        self.__controller = controller
        
    def run_menu(self):
        while True:
            print("1. Run algorithm")
            print("2. Exit")
            opt = int(input())
            if opt == 2:
                break
            if opt == 1:
                loss, fct = self.__controller.runAlgorithm()
                print("Loss = " + str(loss))
                print("Function = " + str(fct))
                
                
            
            
        
ctrl = Controller("data2.txt")
ui = UI(ctrl)
ui.run_menu()    