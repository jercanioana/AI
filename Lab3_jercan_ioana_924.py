# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from itertools import permutations
import random
from random import randint, choice
from copy import deepcopy

        
        
class Individual:
    def __init__(self, size, matrix):
        self.__size = size
        self.__matrix = matrix
        
    def getSize(self):
        return self.__size
    
    
    def getMatrix(self):
        return self.__matrix
    
    def fitness(self):
        f = 0
        for i in range(self.getSize()):
            for j in range(self.getSize()):

                if self.repeatingRow1(i,j, self.__matrix[i][j]):
                    f += 1
                if self.repeatingColumn1(i,j, self.__matrix[i][j]):
                    f += 1 
                if self.repeatingRow2(i,j, self.__matrix[i][j]):
                    f += 1
                if self.repeatingColumn2(i,j, self.__matrix[i][j]):
                    f += 1
                    
        return f
    
   
    def repeatingRow1(self, row,column, value):
        a1,b1 = value
        for i in range(self.getSize()):
            if i != column:
                a,b = self.__matrix[row][i]
                if a == a1:
                    return True
        return False
    
    def repeatingRow2(self,row,column, value):
        a1,b1 = value

        for i in range(self.getSize()):
            if i != column:
                a,b = self.__matrix[row][i]
                if b == b1:
                    return True
        return False
    
    def repeatingColumn1(self,row, column, value):
        a1,b1 = value
        for i in range(self.getSize()):
            if row != i:
                a,b = self.__matrix[i][column]
                if a == a1:
                    return True
        return False
    
    def repeatingColumn2(self, row,column, value):
        a1,b1 = value
        for i in range(self.getSize()):
            if row != i:
                a,b = self.__matrix[i][column]
                if b == b1:
                    return True
        return False
    
    
    

    
class PopulationForEA:
    def __init__(self, length, sizeForIndividual, set1, set2):
        self.__population = []
        self.__length = length
        self.__size = sizeForIndividual
        self.__set1 = set1
        self.__set2 = set2
        self.population()

        
    def getMatrix(self):
        return self.__matrix
        
    def setLength(self, l):
        self.__length = l

    def getLengthForIndividual(self):
        return self.__size
        
    def getLength(self):
        return self.__length
    
    def getPopulation(self):
        return self.__population
    
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
    
    def generateIndividual(self):
        individual = [[(0,0)] * self.__size for i in range(self.__size)]
        p1,p2 = self.getPermutations()
        permutation1 =  p1[random.randint(0,self.__size-1)]
        permutation2 = p2[random.randint(0,self.__size-1)] 
        for i in range(self.__size):
            for j in range(self.__size):
                individual[i][j] = ((permutation1[j]),(permutation2[j]))
            permutation1 =  p1[random.randint(0,self.__size-1)]
            permutation2 = p2[random.randint(0,self.__size-1)] 
        
        individual1 = Individual(self.__size, individual)
        return individual1
        
    def population(self):
        self.__population = [self.generateIndividual() for x in range(self.__length)]
    
    def mutate(self, ind, pM):
        p1,p2 = self.getPermutations()
        permutation1 = p1[random.randint(0,self.__size-1)]
        permutation2 = p2[random.randint(0,self.__size-1)] 
        
        if pM < random.random():
            individual = ind.getMatrix()
            row = random.randint(0, self.__size-1)
            for j in range(self.__size):
                individual[row][j] = ((permutation1[random.randint(0, self.__size-1)]), (permutation2[random.randint(0, self.__size-1)]))
    
            
    def crossover(self, parent1, parent2):
        
        new_child = [[(0,0)]*self.__size for i in range(self.__size)]
        matrix1 = parent1.getMatrix()
        matrix2 = parent2.getMatrix()
        startingPoint1 = random.randint(0, self.__size-2)
        startingPoint2 = random.randint(startingPoint1, self.__size-1)
        
        for i in range (self.__size):
            for j in range (self.__size):
                if i < startingPoint1:
                    elem1, elem2 = matrix1[i][j]
                    new_child[i][j] = matrix1[i][j]
                if i >= startingPoint1 and i < startingPoint2:
                    new_child[i][j] = matrix2[i][j]
                if i >= startingPoint2:
                    new_child[i][j] = matrix1[i][j]
        ind = Individual(self.__size, new_child)
        return ind
        
    def iteration(self, pM):
        i1 = random.randint(0, len(self.__population)-1)
        i2 = random.randint(0, len(self.__population)-1)
        if(i1 != i2):
            c = self.crossover(self.__population[i1], self.__population[i2])
            self.mutate(c, pM)
            f1 = self.__population[i1].fitness()
            f2 = self.__population[i2].fitness()
            fc = c.fitness()
            if(f1>f2) and (f1>fc):
                self.__population[i1]=c
            if(f2>f1) and (f2>fc):
                self.__population[i2]=c
        return self
    
    def generateNeighbours(self, individual):
        neighbours = []
        matrix = individual.getMatrix()
        p1,p2 = self.getPermutations()
        row = random.randint(0, self.__size-1)
        positions1 = []
        positions2 = []
        for x in range(len(p1)):
            pos1 = choice([i for i in range(0, len(p1)) if i not in positions1])
            positions1.append(pos1)
            permutation1 = p1[pos1]
            pos2 = choice([i for i in range(0, len(p2)) if i not in positions2])
            positions2.append(pos2)
            permutation2 = p2[pos2]
            for i in range (self.__size):
                matrix[row][i] = ((permutation1[i]),(permutation2[i]))
            
            matrixInd = Individual(self.__size, matrix)
            neighbours.append(matrixInd)
            
            
        
        return neighbours
    


            
class Controller:
    def __init__(self, population):
        self.__population = population
        
    def HillClimbing(self):
        self.__population.population()
        individual = self.__population.getPopulation()
        aux = Individual(self.__population.getLengthForIndividual(),individual[0].getMatrix())
        
        
        while aux.fitness() != 0:
        
            neighbours = self.__population.generateNeighbours(aux)
            
            solution = [[x, x.fitness()] for x in neighbours]
            solution.sort(key=lambda x:x[1])
            bestIndividual, fitness = solution[0]
            
            
            if aux.fitness() > bestIndividual.fitness():
                aux = bestIndividual
            
        return aux
    
    def EA(self, noOfIterations, pM):
        self.__population.population()
        pop = self.__population.getPopulation()
        for i in range(noOfIterations):
            pop = self.__population.iteration(pM)
        population = pop.getPopulation()
        graded = [ (x.fitness(), x) for x in population]
        graded.sort(key=lambda x:x[0])
        result=graded[0]
        
        return result
class UI:
    def menu(self):
        while True:
            print("Choose method: ")
            method = input()
            if method == "EA":
                print("Probability")
                prob = float(input())
                print("Size of the population: ")
                length = int(input())
                print("Size of the individual: ")
                sizeForIndividual = int(input())
                set1 = [1,2,3]
                set2 = [1,2,3]
                pop = PopulationForEA(length, sizeForIndividual, set1, set2)
                controller = Controller(pop)
                print("Number of iterations")
                it = int(input())
                res, ind = controller.EA(it, prob)
                print(res)
                print(ind.getMatrix())
            if method == "HC":
                length = 1
                print("Size of the individual: ")
                sizeForIndividual = int(input())
                set1 = [1,2,3]
                set2 = [1,2,3]
                pop = PopulationForEA(length, sizeForIndividual, set1, set2)
                controller = Controller(pop)
                res = controller.HillClimbing().getMatrix()
                print(res)
            if method == "Exit":
                break

ui = UI()
ui.run()


            
