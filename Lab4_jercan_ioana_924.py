# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 08:31:23 2020

@author: ioana
"""

from itertools import permutations
import random
from random import randint, choice
from copy import deepcopy
class Particle:
    
    def __init__(self, size, matrix):
        self.__size = size
        self.__position = matrix
        self._fitness = 0
        self.evaluate()
        self._bestFit = self._fitness
        self._bestPosition = self.__position.copy()
        self.velocity = [ [0,0] * self.__size for i in range(self.__size)]
        

    
    def getSize(self):
        return self.__size
    

    def getPosition(self):
        """ getter for position """
        return self.__position

    def getLine(self, i):
        return self.__position[i]
    def bestPosition(self):
        """ getter for best position """
        return self._bestPosition
    
    def fit(self):
        f = 0
        for i in range(self.getSize()):
            for j in range(self.getSize()):

                if self.repeatingRow1(i,j, self.__position[i][j]):
                    f += 1
                if self.repeatingColumn1(i,j, self.__position[i][j]):
                    f += 1 
                if self.repeatingRow2(i,j, self.__position[i][j]):
                    f += 1
                if self.repeatingColumn2(i,j, self.__position[i][j]):
                    f += 1
                    
        return f
    
   
    def repeatingRow1(self, row,column, value):
        a1,b1 = value
        for i in range(self.getSize()):
            if i != column:
                a,b = self.__position[row][i]
                if a == a1:
                    return True
        return False
    
    def repeatingRow2(self,row,column, value):
        a1,b1 = value

        for i in range(self.getSize()):
            if i != column:
                a,b = self.__position[row][i]
                if b == b1:
                    return True
        return False
    
    def repeatingColumn1(self,row, column, value):
        a1,b1 = value
        for i in range(self.getSize()):
            if row != i:
                a,b = self.__position[i][column]
                if a == a1:
                    return True
        return False
    
    def repeatingColumn2(self, row,column, value):
        a1,b1 = value
        for i in range(self.getSize()):
            if row != i:
                a,b = self.__position[i][column]
                if b == b1:
                    return True
        return False
        
    def evaluate(self):
        self._fitness = self.fit()
        

    def setPosition(self, newPosition):
        self.__position=newPosition.copy()
        # automatic evaluation of particle's fitness
        self.evaluate()
        # automatic update of particle's memory
        if (self._fitness<self._bestFitness):
            self._bestPosition = self.__position
            self._bestFit  = self._fitness
            
    def fitness(self):
        """ getter for fitness """
        return self._fitness

    def bestFit(self):
        """ getter for best pozition """
        return self._bestFit
    
    def getBestLine(self, i):
        return self._bestPosition[i]
    
class Population:
    def __init__(self, count, sizeOfParticle, set1, set2):
        
        self.__particles = []
        self.__count = count
        self.__sizeOfParticle = sizeOfParticle
        self.__set1 = set1
        self.__set2 = set2
        
        
        
    def getPopulation(self):
        return self.__particles
    
    def getPermutations(self):
        per = []
        per2 = []
        p1 = permutations(self.__set1)
        for p in p1:
            per.append(p)
        p2 = permutations(self.__set2)
        for p in p2:
            per2.append(p)
         
        return per, per2
    
    def generateParticle(self):
        particle = [[(0,0)] * self.__sizeOfParticle for i in range(self.__sizeOfParticle)]
        p1,p2 = self.getPermutations()
        permutation1 =  p1[random.randint(0,self.__sizeOfParticle-1)]
        permutation2 = p2[random.randint(0,self.__sizeOfParticle-1)] 
        for i in range(self.__sizeOfParticle):
            for j in range(self.__sizeOfParticle):
                particle[i][j] = ((permutation1[j]),(permutation2[j]))
            permutation1 =  p1[random.randint(0,self.__sizeOfParticle-1)]
            permutation2 = p2[random.randint(0,self.__sizeOfParticle-1)] 
        
        particle1 = Particle(self.__sizeOfParticle, particle)
        return particle1   
        
    def population(self):
        self.__particles = [self.generateParticle() for x in range (self.__count)]
        
    
    def selectNeighbours(self, nSize):
        if(nSize > self.__count):
            nSize = self.__count
        neighbours = []
        for i in range (self.__count):
            localNeighbour = []
            for j in range (nSize):
                x = random.randint(0, self.__count-1)
                while x in localNeighbour:
                    x = random.randint(0, self.__count-1)
                localNeighbour.append(x)
            neighbours.append(localNeighbour.copy())
        return neighbours    

    def calculate(self, line1, line2):
        result = []
        for i in range(len(line1)):
            a,b = line1[i]
            c,d = line2[i]
            result.append(((a-c), (b-d)))
        
        return result
    def iteration(self, neighbours, c1, c2, w):
        w = int(w)
        bestNeighbours = []
        for i in range(self.__count):
            bestNeighbours.append(neighbours[i][0])
            for j in range(1, len(neighbours[i])):
                if self.__particles[bestNeighbours[i]].fitness()>self.__particles[neighbours[i][j]].fitness():
                    bestNeighbours[i]=neighbours[i][j]
        
        for i in range(self.__count):
            for j in range(len(self.__particles[0].velocity)):
                newVelocity = w * self.__particles[i].velocity[j]
                newVelocity = newVelocity + c1*random.randint(0,1)*self.calculate(self.__particles[bestNeighbours[i]].getLine(j),self.__particles[i].getLine(j))    
                newVelocity = newVelocity + c2*random.randint(0,1)*self.calculate(self.__particles[i].getBestLine(j),self.__particles[i].getLine(j))
        
        for i in range(self.__count):
            newPosition = []
            for j in range(len(self.__particles[0].velocity)):
                newPosition.append(self.__particles[i].getLine(j)+self.__particles[i].velocity[j])
            self.__particles[i].position = newPosition
        pop = self.__particles
        return pop

class Controller:
    def __init__(self, population):
        self.__population = population
    
    def PSO(self, noOfIterations, nSize, c1, c2, vel):
        self.__population.population()
        neighbours = self.__population.selectNeighbours(nSize)
        for i in range(noOfIterations):
            pop = self.__population.iteration(neighbours, c1, c2, vel)
        best = 0
        for i in range(1, len(pop)):
            if (pop[i].fitness()<pop[best].fitness()):
                best = i
        fitnessOptim=pop[best].fitness()
        individualOptim=pop[best].getPosition()  
        return individualOptim

class UI:
    def menu(self):
        while True:
            print("Enter method: ")
            method = input()
            if method == "Exit":
                break
            if method == "PSO":
                print("Enter size of particle: ")
                sizeOfParticle = int(input())
                print("Size of population: ")
                count = int(input())
                set1 = [1,2,3]
                set2 = [1,2,3]
                population = Population(count, sizeOfParticle, set1, set2)
                contr = Controller(population)
                print("Size of neighbours: ")
                nSize = int(input())
                print("c1 = ")
                c1 = float(input())
                print("c2 = ")
                c2 = float(input())
                print("w = ")
                w = float(input())
                print("Number of iterations = ")
                noOfIterations =  int(input())
                print(contr.PSO(noOfIterations, nSize, c1, c2, w).getMatrix())
                
                
ui = UI()
ui.menu()
            
