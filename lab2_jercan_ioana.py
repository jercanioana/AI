# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 08:08:28 2020

@author: ioana
"""
from copy import deepcopy

class Configuration:
    def __init__(self, size, matrix, row):
        self.__size = size
        self.__values = matrix
        self.__row = row
        
    def getLastValidLine(self):
        return self.__row
    
    def getSize(self):
        return self.__size
    
    def getValues(self):
        return self.__values
    
    def checkDiagonals(self,row,column):
        matrix = self.getValues()
        size = self.getSize()
        
        rowIndex = row-1
        columnIndex = column-1
        while rowIndex >= 0 and columnIndex >= 0:
            if matrix[rowIndex][columnIndex] == 1:
                return False
            rowIndex -= 1
            columnIndex -= 1
            
        rowIndex = row+1
        columnIndex = column+1
        while rowIndex < size and columnIndex < size:
            if matrix[rowIndex][columnIndex] == 1:
                return False
            rowIndex += 1
            columnIndex += 1
  
        rowIndex = row-1
        columnIndex = column+1
        while rowIndex >= 0 and columnIndex < size:
            if matrix[rowIndex][columnIndex] == 1:
                return False
            rowIndex -= 1
            columnIndex += 1

        rowIndex = row+1
        columnIndex = column-1
        while rowIndex < size and columnIndex >= 0:
            if matrix[rowIndex][columnIndex] == 1:
                return False
            rowIndex += 1
            columnIndex -= 1
        return True
        
    
    def verifyColumn(self, row, column):
        for i in range(self.__size):
            if self.__values[i][column] == 1 and row != i:
                return False
        return True
        
    def verifyRow(self, row,column):
       for i in range(self.__size):
           if self.__values[row][i] == 1 and column != i:
               return False
                   
       return True
   
    def checkPosition(self, row, column):
        if self.checkDiagonals(row, column) == True and self.verifyRow(row, column) == True and self.verifyColumn(row, column) == True:
            return True
        return False
        
    def nextConfig(self, newPosition1, newPosition2):
        
         new_matrix = deepcopy(self.__values)
         if self.checkPosition(newPosition1, newPosition2) == True:
             new_matrix[newPosition1][newPosition2] = 1
             nextConf = Configuration(self.getSize(), new_matrix, newPosition1)         
             return nextConf
         return False
     
    def __str__(self):
        return str(self.__values)
       
        
class Problem:
    def __init__(self, initialState, finalState):
        self.__initialConfig = initialState
        self.__finalConfig = finalState        
        
    def getInitialState(self, size):
        
            
        matrix = [[self.__initialConfig for row in range(size)]for column in range(size)]
        initialState = Configuration(size, matrix, -1)
        return initialState
    
    def getFinalState(self):
        return self.__finalConfig
    
    def expand(self, currentConfig, row):
        myList = []
        for j in range(self.__finalConfig):             
            nextConf = currentConfig.nextConfig(row+1,j)
            if nextConf != False:
                myList.append(nextConf)
        return myList
    
    def checkFirstLastPos(self, matrix):
         if matrix[0][0] == 0 and matrix[0][self.getFinalState()-1] == 0:
             return True
         return False
    
    def heuristics(self, state, row, column):
        newConfList = []
        for i in range(len(state)):
            matrix = state[i].getValues()
            if self.checkFirstLastPos(matrix) == True:
                newConfList.append([state[i], abs(matrix[row+1].index(1) - column)])
        return newConfList
    
class Controller:
    def __init__(self, problem):
        self.__problem = problem
        
    def Greedy(self, root):
       node = root 
       for i in range(self.__problem.getFinalState()):
           ConfList = self.__problem.expand(node, node.getLastValidLine())
           if ConfList == []:
               return False
           if node.getLastValidLine() != -1:
               matrix = node.getValues()
               nodeList = self.__problem.heuristics(ConfList, node.getLastValidLine(), matrix[node.getLastValidLine()].index(1))
               nodeList.sort(key = lambda x: x[1])
               node = nodeList[0][0]
           else:
               nodeList = self.__problem.heuristics(ConfList, -1, self.__problem.getFinalState())
               nodeList.sort(key = lambda x: x[1])
               node = nodeList[0][0]
       return node
               
            
    def DFS(self, root):

        toVisit = [root]
        while len(toVisit) > 0:
            node = toVisit.pop()
            if node.getLastValidLine() == self.__problem.getFinalState()-1:
                return node
            for x in self.__problem.expand(node, node.getLastValidLine()):
                toVisit.append(x)
    
        return False
        
    
class UI:
    def __init__(self, n):
        
        self.__problem = Problem(0, n)
        self.__controller = Controller(self.__problem)
    
    def findPathGreedy(self):
        print(str(self.__controller.Greedy(self.__problem.getInitialState(self.__problem.getFinalState()))))
        
    def findPathDFS(self):
        print(str(self.__controller.DFS(self.__problem.getInitialState(self.__problem.getFinalState()))))
        
        
    def menu(self):
        print("0. Exit")
        print("1. Find with Greedy")
        print("2. Find with DFS")
        option = int(input())
        while True:
                if option == 0:
                    break
                if option == 1:
                    self.findPathGreedy()
                    break
                if option == 2:
                    self.findPathDFS()
                    break
            
            
size = int(input())
ui = UI(size)
ui.menu()