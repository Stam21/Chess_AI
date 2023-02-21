# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 14:59:30 2023

@author: Mario
""" 

"""
example board = [[None, Pawn(), None],
                 [Knight(), None, None],
                 [None, King(), Queen()]]
"""

MAX_DEPTH = 3

def getBranchValue(board, color, depth):
    if(depth == MAX_DEPTH):
        boardValue = 0
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] != None:
                    if (board[x][y].getColor()):
                        boardValue =+ board[x][y].getValue()
                    else:
                        boardValue =- board[x][y].getValue()
        
        return boardValue
    
    moves = []
    for x in range(len(board)):
        for y in range(len(board[0])):
            for x1 in range(len(board)):
                for y1 in range(len(board[0])):
                    if (elem.getColor() == color and elem.isValid((x,y),(x1,y1))):
                        tempBoard = board
                        tempBoard[x1][y1] = board[x][y]
                        tempBoard[x][y] = None
                        moves.append(tempBoard)
    
    branchValue = 0
    for elem in moves:
        branchValue =+ getBranchValue(elem, !color, depth+1)
    
    return branchValue

def getMove(board, color):
    
    moves = []
    for x in range(len(board)):
        for y in range(len(board[0])):
            for x1 in range(len(board)):
                for y1 in range(len(board[0])):
                    if (elem.getColor() == color and elem.isValid((x,y),(x1,y1))):
                        tempBoard = board
                        tempBoard[x1][y1] = board[x][y]
                        tempBoard[x][y] = None
                        moves.append(tempBoard)
        
        maxValue = -10000
        maxIndex = -1
        for x in range(len(moves)):
            newValue = getBranchValue(board, color, 0)
            if (newValue > maxValue):
                maxValue = newValue
                maxIndex = x
    
    return moves[maxIndex]
            
        
    