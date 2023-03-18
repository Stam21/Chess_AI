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
import copy
from evaluation_1 import evaluation_1
from evaluation_2 import evaluation_2_attacking, evaluation_2_protecting
from evaluation_3 import evaluation_3
from math import inf


MAX_DEPTH = 1
W1, W2, W3, W4 = 0.75, 0.1, 0.1, 0.05

def getNodeValue(board, isWhite, depth, alpha, beta, next_move):
    str_board = BtG.convertToStrings(board) #convert board
    #terminal codition by depth
    if(depth == MAX_DEPTH):
        boardValue = (W1*evaluation_1(board, isWhite) + 
                      W2*evaluation_2_attacking(str_board, isWhite) + 
                      W3*evaluation_2_protecting(str_board, isWhite) +
                      W4*evaluation_3(board, isWhite)  
                      )
        #print(alpha,beta,boardValue)
        #print("BV", boardValue)
        return boardValue, next_move, beta, alpha
    
    game_table = ChessGame.GameState()
    game_table.board = str_board
    if (depth%2 == 0): #turno de max
        game_table.whiteMove = isWhite
    else: #turno de min
        game_table.whiteMove = not isWhite
    
    moves = game_table.getValidMoves()
    
    #terminal condition by the rules
    if (len(moves) == 0):
        if (len(game_table.threats) == 0):
            print("EMPATE")
            return 0, next_move, beta, alpha
        else:
            if (game_table.whiteMove == isWhite):
                return 10000000000, next_move, beta, alpha
            else:
                return -10000000000, next_move, beta, alpha
            
        
    #intermediate node
    childrenNodes = []
    for move in moves: #transform moves into states
        newBoard = copy.deepcopy(board)
        newBoard[move.startRow][move.startCol] = 0
        newBoard[move.endRow][move.endCol] = board[move.startRow][move.startCol]
        childrenNodes.append(newBoard)
    
    next_move_idx = 0
    child_index = 0
    values = []
    if depth % 2 == 0:  #max's turn
        nodeValue = -inf #algorthim initializes 'nodeValue' to negative value, then next line:
        for child in childrenNodes:  
            # goes deeper into the tree to get the values that come to this node
            # goes thorugh every child node, compute its value in (recurisvely)call to 'getNodeValue'
            call = getNodeValue(child, isWhite, depth + 1, alpha, beta, next_move)
            value = call[0]
            values.append(value)
            alpha = max(call[3], alpha) #beta propagates up as alpha
            #beta = min(call[2], beta)  #alpha propagates up as beta
            #nodeValue = max(nodeValue, value)
            # if the value > current 'nodeValue' then algorthim update'nodeValue'
            alpha = max(alpha, nodeValue) #algorthim also update 'alpha' to maxium its current value and 'nodeValue'
            #print("l", nodeValue, beta)
            if nodeValue < value:
                #print(nodeValue, value, "max")
                nodeValue = value
                next_move_idx = child_index
            #if nodeValue >= beta:
                # if 'v' >= 'beta', means the current node will delet, 
                # and algorithm prune the rest nodes in tree, this done by 'break'
                #break
            child_index += 1

    else: #min's turn
        nodeValue = inf # turn 'nodeValue' into postive infinity
        for child in childrenNodes:  # goes deeper into the tree to get the values that come to this node 
            #go through each child node
            call = getNodeValue(child, isWhite, depth + 1, alpha, beta, next_move)
            value = call[0]
            #alpha = max(call[3], alpha) #beta propagates up as alpha
            beta = min(call[2], beta)  #alpha propagates up as beta
            #nodeValue = min(nodeValue, value) #compute its value using recurisive call to 'getNode' above 
            beta = min(beta, nodeValue)
            if nodeValue > value:
                #print(nodeValue, value, "min")
                nodeValue = value
                next_move_idx = child_index
            #if nodeValue <= alpha:
                #break
            child_index += 1
    #print("alpha:", alpha)
    #print("beta:", beta)
    if depth == 0:
        print(nodeValue)
        print(values)
        print(next_move_idx)
        next_move = moves[next_move_idx]
    
    #print(alpha,beta)
    return nodeValue, next_move, alpha, beta

            
def getNextMove(board, isWhite):
    #numberBoard = BtG.convertToNumbers(board)
    next_move = "NOT YET CALCULATED"
    next_move = getNodeValue(board, isWhite, 0,-inf, inf, next_move)[1]
    return next_move
        
initialBoard = [[10,8,9,11,12,9,8,10],
                [7,7,7,7,7,7,7,7],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1],
                [4,2,3,5,6,3,2,4]]

print(getNextMove(initialBoard, True).getChessNotation())