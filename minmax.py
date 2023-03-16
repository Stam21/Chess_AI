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
import adaptationBackboneToGUI as BtG

MAX_DEPTH = 1
W1, W2, W3 = 0.6, 0.3, 0.1

####################MOCKS#######################

def utility_1(board):
    return 0.7

def utility_2(board):
    return -0.7

def utility_3(board):
    return 1
################################################

def getNodeValue(board, isWhite, depth, next_move):
    #terminal codition by depth
    if(depth == MAX_DEPTH):
        
        boardValue = W1*utility_1(board) + W2*utility_2(board) + W3*utility_3(board)
        return boardValue, next_move
    
    game_table = ChessGame.GameState()
    str_board = BtG.convertToStrings(board) #convert board
    game_table.board = str_board
    if (depth%2 == 0): #turno de max
        game_table.whiteMove = isWhite
    else: #turno de min
        game_table.whiteMove = not isWhite
    
    moves = game_table.getValidMoves()
    
    #terminal condition by the rules
    if (len(moves) == 0):
        if (len(game_table.threats) == 0):
            return 0, next_move
        else:
            if (game_table.whiteMove == isWhite):
                return 10000000000, next_move
            else:
                return -10000000000, next_move
            
        
    #intermediate node
    childrenNodes = []
    for move in moves: #transform moves into states
        newBoard = board.copy()
        newBoard[move.startRow][move.startCol] = 0
        newBoard[move.endRow][move.endCol] = board[move.startRow][move.startCol]
        childrenNodes.append(newBoard)
    
    childrenValues = []
    for child in childrenNodes: #goes deeper into the tree to get the values that come to this node
        value = getNodeValue(child, isWhite, depth, next_move)[0]
        childrenValues.append(value)
    
    if (depth%2 == 0): #turn of max
        nodeValue = max(childrenValues)
    else:              #turn of min
        nodeValue = min(childrenValues)
        
    if depth == 0:
        idx = childrenValues.index(nodeValue)
        next_move = moves[idx]
    
    return nodeValue, next_move

            
def getNextMove(board, isWhite):
    next_move = "NOT YET CALCULATED"
    next_move = getNodeValue(board, isWhite, 0, next_move)[1]
    return next_move
        
initialBoard = [[10,8,9,11,12,9,8,10],
                [7,7,7,7,7,7,7,7],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1],
                [4,2,3,5,6,3,2,4]]
