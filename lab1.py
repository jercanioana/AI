# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 12:40:41 2020

@author: ioana
"""
import numpy
import matplotlib.pyplot as plt

while True:
    print("Choose a distribution:")
    print("1.Uniform")
    print("2.Binomial")
    print("3.Exit")
    type_of_distribution = int(input())
    if type_of_distribution == 1:
        print("Enter lower bound: ")
        lowerbound = int(input())
        print("Enter upper bound: ")
        upperbound = int(input())
        a = numpy.random.uniform(lowerbound,upperbound,10)
        plt.title("Uniform distribution")
        plt.plot(a, 'ro')
        plt.show()
        
    elif type_of_distribution == 2:
        n = 10
        p = 0.35
        s = numpy.random.binomial(n,p,10)
        plt.title("Binomial distribution")
        plt.plot(s, 'ro')
        plt.show()
    else:
        break


