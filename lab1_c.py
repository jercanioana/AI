# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:01:44 2020

@author: ioana
"""
import numpy as np
import math
import copy
from random import choice



def menu():
    while(True):
        print("1. Sudoku")
        print("2. Cryptarithmetic game")
        print("3. Geometric forms")
        print("4. Exit")
        print("Choose and option: ")
        command = int(input())
        if command == 1:
            sudoku()
        if command == 2:
            cryptography()
        if command == 3:
            geometricForms()
        if command == 4:
            break
        
def sudoku():
    
    def start():
          while True:
              print("1. 4x4 game")
              print("2. 9x9 game")
              print("3. Exit")
              version = int(input())
              if version == 3:
                  break
              print("How many attempts?")
              attempts = int(input())
              if(version == 1):
                  size = 4
                  board = np.array([[3,-1,-1,2],[-1,1,4,-1],[1,2,-1,4],[-1,3,2,1]])
                  while attempts > 0:
                     new_board = copy.deepcopy(board)
                     bb = generateBoard(size,new_board)
                     trial = solveSudoku(size, bb)
                     if trial != False:
                         print(bb)
                         break
                     attempts-= 1
              if(version == 2):
                  size = 9
                  board = np.array([[-1,2,-1,6,-1,8,-1,-1,5],
                                    [5,8,-1,-1,-1,9,7,-1,-1],
                                    [-1,-1,7,-1,4,-1,-1,2,8],
                                    [3,7,-1,4,-1,1,5,-1,-1],
                                    [6,-1,-1,-1,8,-1,-1,-1,5],
                                    [-1,-1,8,-1,-1,2,-1,1,3],
                                    [8,-1,6,-1,2,-1,1,-1,-1],
                                    [-1,-1,9,8,-1,-1,-1,3,6],
                                    [7,-1,-1,3,-1,6,-1,9,-1]])
                  while attempts > 0:
                     new_board = copy.deepcopy(board)
                     bb = generateBoard(size,new_board)
                     trail = solveSudoku(size, bb)
                     if trail != False:
                         print(bb)
                     attempts-= 1
                
    def generateBoard(size, board):
        
        for i in range(0, size):
            for j in range(0, size):
                if board[i][j] == -1:
                    board[i][j] = np.random.randint(1, size+1)
    
        return board
    
    def checkIfSolution(size,board,row, column, number):
        for column_index in range(0, size):
            if board[row][column_index] == number and column_index != column:
                return False
        for row_index in range(0, size):
            if board[row_index][column] == number and row_index != row:
                return False
        
        new_row = (row // int(math.sqrt(size))) * int(math.sqrt(size))
        new_column = (column // int(math.sqrt(size))) * int(math.sqrt(size))
        
        for row_index in range(0, int(math.sqrt(size))):
            for column_index in range(0, int(math.sqrt(size))):
                if new_row + row_index != row and new_column + column_index != column and board[new_row+row_index][new_column+column_index] == number:
                    return False
        return True
        
            
    
    def solveSudoku(size,board):
        for row in range(0, size):
            for column in range(0, size):
                if checkIfSolution(size, board, row, column, board[row][column]) == False:
                    return False
                    
        return True
    start()


def cryptography():
    def generatingLettersForOption1(crypto):
        
        crypto["E"] = np.random.randint(0,16)
        crypto["D"] = choice([i for i in range (0,16) if i not in crypto.values()])
        crypto["M"] = choice([i for i in range (1,16) if i not in crypto.values()])
        crypto["R"] = choice([i for i in range (0,16) if i not in crypto.values()])
        crypto["O"] = choice([i for i in range (0,16) if i not in crypto.values()])
        crypto["Y"] = choice([i for i in range (0,16) if i not in crypto.values()])
        crypto["N"] = choice([i for i in range (0,16) if i not in crypto.values()])
        crypto["S"] = choice([i for i in range (1,16) if i not in crypto.values()])
        
        return crypto
        
    def generatingLettersForOption2(crypto):
        crypto["T"] = np.random.randint(1,16)
        crypto["A"] = choice([i for i in range (1,16) if i not in crypto.values()])
        crypto["K"] = choice([i for i in range (1,16) if i not in crypto.values()])         
        crypto["E"] = choice([i for i in range (0,16) if i not in crypto.values()])
        crypto["C"] = choice([i for i in range (1,16) if i not in crypto.values()])
        return crypto
    
    def generatingLettersForOption3(crypto):
        crypto["T"] = np.random.randint(1,16)
        crypto["A"] = choice([i for i in range (1,16) if i not in crypto.values()])
        crypto["P"] = choice([i for i in range (0,16) if i not in crypto.values()])         
        crypto["E"] = choice([i for i in range (1,16) if i not in crypto.values()])
        crypto["L"] = choice([i for i in range (0,16) if i not in crypto.values()])
        crypto["H"] = choice([i for i in range (0,16) if i not in crypto.values()])
        return crypto
    
    def generatingLettersForOption4(crypto):
        crypto["N"] = np.random.randint(1,16)
        crypto["V"] = choice([i for i in range (0,16) if i not in crypto.values()])
        crypto["R"] = choice([i for i in range (1,16) if i not in crypto.values()])         
        crypto["E"] = choice([i for i in range (0,16) if i not in crypto.values()])
        crypto["D"] = choice([i for i in range (1,16) if i not in crypto.values()])
        crypto["I"] = choice([i for i in range (0,16) if i not in crypto.values()])
        return crypto
        
    def checkResult1(crypto):
        first_word = crypto["D"] + crypto["N"] * 16 + crypto["E"] * 16 ** 2 + crypto["S"] * 16 ** 3
        second_word = crypto["E"] + crypto["R"] * 16 + crypto["O"] * 16 **2 + crypto["M"] * 16 ** 3
        first_result = first_word + second_word
        second_result = crypto["Y"] + crypto["E"] * 16 + crypto["N"] * 16 ** 2 + crypto["O"] * 16 ** 3 + crypto["M"] * 16 ** 4
        if first_result != second_result:
            return False
        else:
            return True
        
    def checkResult2(crypto):
        first_word = crypto["E"] + crypto["K"] * 16 + crypto["A"] * 16 ** 2 + crypto["T"] * 16 ** 3
        second_word = crypto["A"]
        third_word = crypto["E"] + crypto["K"] * 16 + crypto["A"] * 16 **2 + crypto["C"] * 16 ** 3
        first_result = first_word + second_word + third_word
        second_result = crypto["E"] + crypto["T"] * 16 + crypto["A"] * 16 ** 2 + crypto["K"] * 16 ** 3
        if first_result != second_result:
            return False
        else:
            return True
        
    def checkResult3(crypto):
        first_word = crypto["T"] + crypto["A"] * 16 + crypto["E"] * 16 ** 2
        second_word = crypto["T"] + crypto["A"] * 16 + crypto["H"] * 16 ** 2 + crypto["T"] * 16 ** 3
        
        first_result = first_word + second_word
        second_result = crypto["E"] + crypto["L"] * 16 + crypto["L"] * 16 **2 + crypto["P"] * 16 ** 3 + crypto["A"] * 16 ** 4
        if first_result != second_result:
            return False
        else:
            return True
        
    def checkResult4(crypto):
        first_word = crypto["R"] + crypto["E"] * 16 + crypto["V"] * 16 ** 2 + crypto["E"] * 16 ** 3 + crypto["N"] * 16 ** 4
        second_word = crypto["E"] + crypto["I"] * 16 + crypto["V"] * 16 ** 2 + crypto["R"] * 16 ** 3 + crypto["D"] * 16 ** 4
        if first_word < second_word:
            return False
        first_result = first_word - second_word
        second_result = crypto["E"] + crypto["D"] * 16 + crypto["I"] * 16 **2 + crypto["R"] * 16 ** 3
        if first_result != second_result:
            return False
        else:
            return True
    
    def start():
        while True:
            print("Choose a game: ")
            print("1: SEND + MORE = MONEY")
            print("2: TAKE + A + CAKE = KATE")
            print("3: EAT + THAT = APPLE")
            print("4: NEVER - DRIVE = RIDE")
            print("5. Exit")
            option = int(input())
            if option == 5:
                break
            print("How many attempts?")
            attempts = int(input())
            if option == 1:
                crypto = {"E":0,"D":0,"M":0,"R":0,"O":0,"Y":0,"N":0,"S":0}
                while attempts > 0:
                    c = generatingLettersForOption1(crypto)
                    result = checkResult1(c)
                    if result == True:
                        print(c)
                        break
                    attempts -= 1
                if result == False:
                    print("No solution")
            if option == 2:
                crypto = {"T":0, "A":0, "K":0, "E": 0, "C":0}
                while attempts > 0:
                    c = generatingLettersForOption2(crypto)
                    result = checkResult2(c)
                    if result == True:
                        print(c)
                        break
                    attempts -= 1
                if result == False:
                    print("No solution")
            if option == 3:
                crypto = {"T":0, "A":0, "H":0, "E": 0, "A":0, "P":0, "L":0}
                while attempts > 0:
                    c = generatingLettersForOption3(crypto)
                    result = checkResult3(c)
                    if result == True:
                        print(c)
                        break
                    attempts -= 1
                if result == False:
                    print("No solution")
            if option == 4:
                crypto = {"N":0, "E":0, "V":0, "R": 0, "I":0, "D":0}
                while attempts > 0:
                    c = generatingLettersForOption4(crypto)
                    result = checkResult4(c)
                    if result == True:
                        print(c)
                        break
                    attempts -= 1
                if result == False:
                    print("No solution")
            
    start()  

def geometricForms():
    global board
    def start():
        board = np.array([[0,0,0,0,0,0],
                         [0,0,0,0,0,0],
                         [0,0,0,0,0,0],
                         [0,0,0,0,0,0],
                         [0,0,0,0,0,0],
                         ])
        print("How many attempts?")
        attempts = int(input())
        while attempts > 0:
            board_copy = copy.deepcopy(board)
            result = addPieces(board_copy)
            if result == True:
                print(board_copy)
                break
            attempts -= 1
            
        if result == False:
            print("No solution found")
        
    def generatePiece1(board):
        aux_board = copy.deepcopy(board)
        row = np.random.randint(0,5)
        column = np.random.randint(0,6)
        if board[row][column] == 0:
            board[row][column] = 1

            if column+1 < 6 and board[row][column+1] == 0:
                board[row][column+1] = 1
                if  column+2 < 6 and board[row][column+2] == 0:
                    board[row][column+2] = 1
                    if column+3 < 6 and board[row][column+3] == 0:
                        board[row][column+3] = 1
                        return True
                    else:
                        board = aux_board
                        return False
                    board = aux_board
                    return False
                board = aux_board
                return False
            board = aux_board
            return False
        board = aux_board
        return False
        
    def generatePiece2(board):
        aux_board = copy.deepcopy(board)
        row = np.random.randint(0,5)
        column = np.random.randint(0,6)
        if board[row][column] == 0:
            board[row][column] = 2
            if  column < 6 and row-1 > 0 and board[row-1][column] == 0:
                board[row-1][column] = 2
                if column+1 < 6 and board[row][column+1] == 0:
                    board[row][column+1] = 2
                    if column+2 < 6 and board[row][column+2] == 0:
                        board[row][column+2] = 2
                        return True
                    else:
                        board = aux_board
                        return False
                    board = aux_board
                    return False
                board = aux_board
                return False
            board = aux_board
            return False
        board = aux_board
        return False
    
    def generatePiece3(board):
        aux_board = copy.deepcopy(board)
        row = np.random.randint(0,5)
        column = np.random.randint(0,6)
        if board[row][column] == 0:
            board[row][column] = 3
            if column < 6 and row-1 > 0 and board[row-1][column] == 0:
                board[row-1][column] = 3
                if column+1 < 6 and board[row][column+1] == 0:
                    board[row][column+1] = 3
                    if column+2 < 6 and board[row][column+2] == 0:
                        board[row][column+2] = 3
                        if row-1 > 0 and column+2 < 6 and board[row-1][column+2] == 0:
                            board[row-1][column+2] = 3
                            return True
                        else:
                            board = aux_board
                            return False
                    board = aux_board
                    return False
                board = aux_board
                return False
            board = aux_board
            return False
        board = aux_board
        return False
    
    def generatePiece4(board):
        aux_board = copy.deepcopy(board)
        row = np.random.randint(0,5)
        column = np.random.randint(0,6)
        if board[row][column] == 0:
            board[row][column] = 4
            if column+1 < 6 and board[row][column+1] == 0:
                board[row][column+1] = 4
                if column+2 < 6 and board[row][column+2] == 0:
                    board[row][column+2] = 4
                    if row+1 < 5 and column+2 < 6 and board[row+1][column+2] == 0:
                        board[row+1][column+2] = 4
                        return True
                    else:
                        board = aux_board
                        return False
                    board = aux_board
                    return False
                board = aux_board
                return False
            board = aux_board
            return False
        board = aux_board
        return False
        
    def generatePiece5(board):
        aux_board = copy.deepcopy(board)
        row = np.random.randint(0,5)
        column = np.random.randint(0,6)
        if board[row][column] == 0:
            board[row][column] = 5
            if column+1 < 6 and board[row][column+1] == 0:
                board[row][column+1] = 5
                if row-1 > 0 and column+1 < 6 and board[row-1][column+1] == 0:
                    board[row-1][column+1] = 5
                    if row < 5 and column+2 < 6 and board[row][column+2] == 0:
                        board[row][column+2] = 5
                        return True
                    else:
                        board = aux_board
                        return False
                    board = aux_board
                    return False
                board = aux_board
                return False
            board = aux_board
            return False
        board = aux_board
        return False
    
    def addPieces(board):
        usedPieces = 0
        properlyFilled = generatePiece1(board)
        usedPieces += 1
        
        if properlyFilled == True:
            properlyFilled = generatePiece2(board)
            usedPieces += 1
            
            if properlyFilled == True:
                properlyFilled = generatePiece3(board)
                usedPieces += 1
                
                if properlyFilled == True:
                    properlyFilled = generatePiece4(board)
                    usedPieces += 1
                    
                    if properlyFilled == True:
                        properlyFilled = generatePiece5(board)
                        usedPieces += 1
                        
        if usedPieces == 5 and properlyFilled == True:
            return True
        else:
            return False
        
    start()
            
        
menu()
        
        