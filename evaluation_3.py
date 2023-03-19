# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:52:05 2023

@author: Mario
"""

"""code based on https://www.chessprogramming.org/Simplified_Evaluation_Function"""


PIECE_BOARDS = {
    1: [[0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]],
    
    2: [[-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]],
    
    3: [[-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]],
    
    4: [[ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 0,  0,  0,  5,  5,  0,  0,  0]],
    
    5: [[-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [ -5,  0,  5,  5,  5,  5,  0, -5],
        [ 0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]],
    
    0: [[[-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [ 20, 20,  0,  0,  0,  0, 20, 20],
        [ 20, 30, 10,  0,  0, 10, 30, 20]],
    
        [[-50,-40,-30,-20,-20,-30,-40,-50],
        [-30,-20,-10,  0,  0,-10,-20,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-30,  0,  0,  0,  0,-30,-30],
        [-50,-30,-30,-30,-30,-30,-30,-50]]]
    }

test_board = [[10, 8, 9,11,12, 9, 8,10],
              [ 7, 7, 7, 7, 7, 7, 7, 7],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 1, 1, 1, 1, 1, 1, 1, 1],
              [ 4, 2, 3, 5, 6, 3, 2, 4]]

# this function will return 0 if we consider it is the beginning of the game and
# 1 if we consider to be on the endgame
def getGameStage(board,isWhite):
    cnt_w=0
    cnt_b = 0
    for x in range(len(board)):
       for y in range(len(board[x])):
           if (int((board[x][y] - 1) / 6) == 0):
               if (board[x][y] == 5):
                   for x1 in range(len(board)):
                       for y1 in range(len(board[x1])):
                           if (x1 != x and y1 != y):
                               if (board[x][y] == 5 or board[x][y] == 6):
                                   return 0
                               elif (board[x][y] == 1 or board[x][y] == 2 or board[x][y] == 3 or board[x][y] == 4):
                                   cnt_w=cnt_w+1
           else:
               if (board[x][y]%6 == 5):
                   for x1 in range(len(board)):
                       for y1 in range(len(board[x1])):
                           if (x1 != x and y1 != y):
                               if (board[x][y]%6 == 5 or board[x][y]%6 == 6):
                                   return 0
                               elif (board[x][y]%6 == 1 or board[x][y]%6 == 2 or board[x][y]%6 == 3 or board[x][y]%6 == 4):
                                   cnt_b = cnt_b + 1
    if(cnt_w<=1 or cnt_b<=1):
        return 1
    else:
       return 0

# this function assigns a value to all pieces based on their position on the board
def evaluation_3(board, isWhite):
    whites = 0
    blacks = 0
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] != 0: 
                if (int((board[x][y]-1)/6) == 0):
                    if (board[x][y]%6 != 0):
                        whites = whites + PIECE_BOARDS[board[x][y]%6][7-x][7-y]
                    else:
                        whites = whites + PIECE_BOARDS[0][getGameStage(board,isWhite)][7-x][7-y]
                else:
                    if (board[x][y]%6 != 0):
                        blacks = blacks + PIECE_BOARDS[board[x][y]%6][x][y]
                    else:
                        blacks = blacks + PIECE_BOARDS[0][getGameStage(board,isWhite)][x][y]
    if (isWhite):
        retval = whites - blacks
    else:
        retval = blacks - whites
    return retval/500
            
print(evaluation_3(test_board, False))


#evaluation_3(test_board, True)
    