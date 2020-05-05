# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 08:04:09 2020

@author: ioana
"""
import random
from itertools import permutations
from random import choice
class Ant:
    def __init__(self, size, set1, set2):
        self.size = size
        self.set1 = set1
        self.set2 = set2
        self.matrix = [[(0,0)] * self.size for x in range(self.size)]
        self.path = [(((random.randint(0,self.size-1)), (random.randint(0,self.size-1))))]

     
    def getSize(self):
        return self.size
    def fitness(self):
        f = 0
        for i in range(self.size):
            for j in range(self.size):

                if self.repeatingRow1(i,j, self.matrix[i][j]):
                    f += 1
                if self.repeatingColumn1(i,j, self.matrix[i][j]):
                    f += 1 
                if self.repeatingRow2(i,j, self.matrix[i][j]):
                    f += 1
                if self.repeatingColumn2(i,j, self.matrix[i][j]):
                    f += 1
                    
        return f
    
    def repeatingRow1(self, row,column, value):
        a1,b1 = value
        for i in range(self.getSize()):
            if i != column:
                a,b = self.matrix[row][i]
                if a == a1:
                    return True
        return False
    
    def repeatingRow2(self,row,column, value):
        a1,b1 = value

        for i in range(self.getSize()):
            if i != column:
                a,b = self.matrix[row][i]
                if b == b1:
                    return True
        return False
    
    def repeatingColumn1(self,row, column, value):
        a1,b1 = value
        for i in range(self.getSize()):
            if row != i:
                a,b = self.matrix[i][column]
                if a == a1:
                    return True
        return False
    
    def repeatingColumn2(self, row,column, value):
        a1,b1 = value
        for i in range(self.getSize()):
            if row != i:
                a,b = self.matrix[i][column]
                if b == b1:
                    return True
        return False
    
    def getPermutations(self):
        per = []
        per2 = []
        p1 = permutations(self.set1)
        for p in p1:
            per.append(p)
        p2 = permutations(self.set2)
        for p in p2:
            per2.append(p)
         
        return per, per2
    
    def nextMove(self, poz):
        p1, p2 = self.getPermutations()
        new = []
        row, column = poz
        permutation1 =  p1[random.randint(0,self.size-1)]
        permutation2 = p2[random.randint(0,self.size-1)]
        variationX = [-1, -1, -1, 0, 1, 1, 1, 0]
        variationY = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(8):
            nextX = row + variationX[i]
            nextY = column + variationY[i]
            if nextX >= 0 and nextX < self.size and nextY >= 0 and nextY < self.size:
                value1, value2 = permutation1[random.randint(len(permutation1)-1)], permutation2[random.randint(len(permutation2)-1)]
                auxValue = self.matrix[row][column]
                self.matrix[row][column] = (value1, value2)
                if self.fitness() == 0 and (nextX, nextY, (value1, value2)) not in self.path:
                    new.append((nextX, nextY, (value1, value2)))
                self.matrix[row][column] = auxValue
            permutation1 = p1[random.randint(0,self.size-1)]
            permutation2 = p2[random.randint(0,self.size-1)]
        return new.deepcopy()
    
    def distMove(self, a):
        dummy=Ant(self.size, self.set1, self.set2)
        dummy.path=self.path.deepcopy()
        dummy.path.append(a)
        return (9-len(dummy.nextMoves(a)))
        
    def addMove(self, q0, trace, alpha, beta):
        
        p = [0 for i in range(self.size * self.size)]
        pair = ((self.path[len(self.path)-1][0]), (self.path[len(self.path)-1][1]))
        nextSteps = self.nextMove(pair).deepcopy()
        
        if (len(nextSteps) == 0):
            return False
        
        for i in nextSteps:
            p[i] = self.distMove(i)
        
        p=[ (p[i]**beta)*(trace[self.path[-1]][i]**alpha) for i in range(len(p))]
        if (random.random()<q0):
           
            p = [ [i, p[i]] for i in range(len(p)) ]
            p = max(p, key=lambda a: a[1])
            self.path.append(nextSteps(p[0]))
            step = nextSteps(p[0])
            self.matrix[step[0]][step[1]] = step[2]

        else:
            
            s = sum(p)
            if s==0:
                return choice(nextSteps)
            p = [ p[i]/s for i in range(len(p)) ]
            p = [ sum(p[0:i+1]) for i in range(len(p)) ]
            r=random.random()
            i=0
            while (r > p[i]):
                i=i+1
            self.path.append(nextSteps[i])
            step = nextSteps(p[0])
            self.matrix[step[0]][step[1]] = step[2]
        return True
    
class Controller:
    def __init__(self, noOfAnts, sizeOfAnt, set1, set2, trace):
        self.population = []
        self.noOfAnts = noOfAnts
        self.sizeOfAnt = sizeOfAnt
        self.trace = trace
        self.set1 = set1
        self.set2 = set2
        
    def antSet(self):
       self.population = [Ant(self.sizeOfAnt,self.set1, self.set2) for i in range(self.noOfAnts)]
        
    def iteration(self, q0, alpha, beta):
      
       for x in self.population:
           x.addMove(q0, self.trace, alpha, beta)
      
    def runAlgorithm(self,q0, alpha, beta,noOfIterations,rho):
        self.antSet()
        for i in range(noOfIterations):
            self.iteration(q0, alpha, beta)
        dTrace=[ 1.0 / self.population[i].fitness() for i in range(self.noOfAnts)]
        for i in range(self.sizeOfAnt ** 2):
            for j in range (self.sizeOfAnt ** 2):
                self.trace[i][j] = (1 - rho) * self.trace[i][j]
        for i in range(self.noOfAnts):
            for j in range(len(self.population[i].path)-1):
                x = self.population[i].path[j][0] * self.sizeOfAnt + self.population[i].path[j][1]
                y = self.population[i].path[j+1][0] * self.sizeOfAnt + self.population[i].path[j+1][1]
                self.trace[x][y] = self.trace[x][y] + dTrace[i]

        f=[ [self.population[i].fitness(), i] for i in range(self.noOfAnts)]
        f=max(f)
        return self.population[f[1]].path
        
                             
class Problem:
    def __init__(self, ctrl):
        self.__controller = ctrl
        
    def setCtrl(self, ctrl):
        self.__controller = ctrl
        
    def loadProblem(self, noOfIterations, noEpoch, q0, alpha, beta, rho):
         sol=[]
         bestSol=[]
         trace=[[1 for i in range(self.__controller.sizeOfAnt ** 2)] for j in range (self.__controller.sizeOfAnt ** 2)]
         for i in range(noEpoch):
             sol=self.__controller.runAlgorithm(q0, alpha, beta,noOfIterations, rho).deepcopy()
             if len(sol)>len(bestSol):
                 bestSol=sol.deepcopy()
                 
class UI:
        
    def menu(self):
        while True:
            print("1: ACO")
            print("0: Exit")
            option = int(input())
            if option == 0:
                break
            if option == 1:
                print("Enter size of ant: ")
                sizeOfAnt = int(input())
                print("Enter size of population: ")
                size = int(input())
                ctrl = Controller(size, sizeOfAnt, [1,2,3], [1,2,3], [])
                print("noEpoch = ")
                noEpoch = int(input())
                print("q0 = ")
                q0 = float(input())
                print("alpha = ")
                alpha = float(input())
                print("beta = ")
                beta = float(input())
                print("rho = ")
                rho = float(input())
                print("Number of iterations: ")
                noOfIt = int(input())
                problem = Problem(ctrl)
                problem.loadProblem(noOfIt, noEpoch, q0, alpha, beta, rho)

ui = UI()
ui.menu()