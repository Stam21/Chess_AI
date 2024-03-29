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
import numpy as np
import adaptationBackboneToGUI as BtG
import copy
from evaluation_1 import evaluation_1
from evaluation_2 import evaluation_2_attacking, evaluation_2_protecting
from evaluation_3 import evaluation_3


MAX_DEPTH = [2]
W1, W2, W3, W4 = 0.4, 0.2, 0.2, 0.2

def getNodeValue(board, isWhite, depth, next_move, alpha, beta):
    str_board = BtG.convertToStrings(board) #convert board
    #terminal codition by depth
    if(depth == MAX_DEPTH[0]):
        boardValue = (W1*evaluation_1(board, isWhite) + 
                      W2*evaluation_2_attacking(str_board, isWhite) + 
                      W3*evaluation_2_protecting(str_board, isWhite) +
                      W4*evaluation_3(board, isWhite)  
                      )
        
        return boardValue, next_move, beta, alpha #in end nodes alpha and beta do not propagate up
    
    game_table = ChessGame.GameState()
    game_table.board = str_board
    if (depth%2 == 0): #turno de max
        game_table.whiteMove = isWhite
    else:              #turno de min
        game_table.whiteMove = not isWhite
    
    moves = game_table.getValidMoves()
    
    #terminal condition by the rules
    if (len(moves) == 0):
        if (len(game_table.threats) == 0):
            return 0, next_move, beta, alpha #in end nodes alpha and beta do not propagate up
        else:
            if (game_table.whiteMove == isWhite):
                return -1000000, next_move, beta, alpha #in end nodes alpha and beta do not propagate up 
            else:
                return 1000000, next_move, beta, alpha #in end nodes alpha and beta do not propagate up
            
        
    #intermediate node
    childrenNodes = []
    for move in moves: #transform moves into states
        newBoard = copy.deepcopy(board)
        newBoard[move.startRow][move.startCol] = 0
        newBoard[move.endRow][move.endCol] = board[move.startRow][move.startCol]
        childrenNodes.append(newBoard)
    
    #prunning
    if (depth%2 == 0): #turn of max
        nodeValue = -100000000
    else:              #turn of min
        nodeValue = 100000000
        
        
    childrenValues = []
    next_move_index = -1
    curent_child_index = 0
    for child in childrenNodes: #goes deeper into the tree to get the values that come to this node
        call = getNodeValue(child, isWhite, depth+1, next_move, alpha, beta)
        value = call[0]
        childrenValues.append(value)
        bottomUPAlpha = call[3] #beta propagates to alpha
        bottomUPBeta = call[2]  #alpha propagates to beta
        
    
        if (depth%2 == 0): #turn of max
            if bottomUPAlpha > alpha:
                alpha = bottomUPAlpha
            alpha = max(alpha, value)
            if (value > nodeValue):
                next_move_index = curent_child_index
                nodeValue = value
            if(nodeValue >= beta):
                break
            
        else:              #turn of min
            if bottomUPBeta < beta:
                beta = bottomUPBeta
            beta = min(beta, value)
            if (value < nodeValue):
                next_move_index = curent_child_index
                nodeValue = value
            if(nodeValue <= alpha):
                    break
                
        curent_child_index = curent_child_index + 1
    
    
    if depth == 0:
        next_move = moves[next_move_index]
    
    return nodeValue, next_move, alpha, beta

            
def getNextMove(board, isWhite):
    pieces = 64
    for row in board:
        pieces = pieces - np.count_nonzero(row == "--")
    MAX_DEPTH[0] = 2 + int((32-pieces)/15)
    numberBoard = BtG.convertToNumbers(board)
    next_move = "NOT YET CALCULATED"
    next_move = getNodeValue(numberBoard, isWhite, 0, next_move, -1000000, 1000000)[1]
    return next_move
        
initialBoard = [[10,8,9,11,12,9,8,10],
                [7,7,7,7,7,7,7,7],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1],
                [4,2,3,5,6,3,2,4]]

#print(getNextMove(initialBoard, True).getChessNotation())