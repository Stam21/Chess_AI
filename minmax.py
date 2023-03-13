# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 14:59:30 2023

@author: Mario
""" 

"""
example board = [[1, 6, 1],
                 [0, 0, 0],
                 [7, 12,7]]
"""

import ChessGame

MAX_DEPTH = 3

####################MOCKS#######################

def utility_1(board):
    return 0.7

def utility_2(board):
    return -0.7

def utility_3(board):
    return 1
################################################

def getNodeValue(board, isWhite, depth, next_move):
    #terminal codition
    if(depth == MAX_DEPTH):
        w1, w2, w3 = 0.6, 0.3, 0.1
        boardValue = w1*utility_1(board) + w2*utility_2(board) + w3*utility_3(board)
        return boardValue, next_move
    
    #intermediate node
    game_table = ChessGame.GameState()
    game_table.board = board
    if (depth%2 == 0): #turno de max
        game_table.whiteMove = isWhite
    else: #turno de min
        game_table.whiteMove = not isWhite
    
    moves = game_table.getValidMoves()
    childrenNodes = []
    for move in moves: #transform moves into states
        newBoard = board
        newBoard[move.startRow][move.startCol] = 0
        newBoard[move.endRow][move.endCol] = board[move.startRow][move.startCol]
        childrenNodes.append(newBoard)
    
    childrenValues = []
    for child in childrenNodes: #goes deeper into the tree to get the values that come to this node
        value = getNodeValue(child, isWhite, depth)[0]
        childrenValues.append(value)
    
    
    if (depth%2 == 0): #turno de max
        nodeValue = max(childrenValues)
    else:              #turno de min
        nodeValue = min(childrenValues)
        
    if depth == 0:
        idx = childrenValues.index(nodeValue)
        next_move = moves[idx]
    
    return nodeValue, next_move

            
def getNextMove(board, isWhite, depth):
    next_move = "NOT YET CALCULATED"
    next_move = getNodeValue(board, isWhite, depth, next_move)[1]
    return next_move
        
    