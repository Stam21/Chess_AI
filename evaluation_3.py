# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:52:05 2023

@author: Mario
"""
import math as mt


test_board = [[10,8,9,11,12,9,8,10],
             [7,7,7,7,7,7,7,7],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0],
             [1,1,1,1,1,1,1,1],
             [4,2,3,5,6,3,2,4]]

def getDistance(pos, center):
    return mt.sqrt(((pos[0] - center[0])**2) + ((pos[1] - center[1])**2))


# this evaluation function takes into consideration the average distance of all
# the pieces of each player to the center of the board.
def evaluation_3(board, isWhite):
    whites = 0
    blacks = 0
    cw = 0
    cb = 0
    for x in range(len(board)):
        for y in range(len(board[0])):
            if (int((board[x][y]-1)/6) == 0 and board[x][y]!=0):
                cw = cw+1
                whites = whites + getDistance((x,y),((len(board)-1)/2,(len(board[0])-1)/2))
            elif (board[x][y]!=0):
                cb = cb+1
                blacks = blacks + getDistance((x,y),((len(board)-1)/2,(len(board[0])-1)/2))
    retval = 0
    whites = 5 - whites/cw
    blacks = 5 - blacks/cb
    if (isWhite):
        retval = whites - blacks
    else:
        retval = blacks - whites
    return retval/5
            


#evaluation_3(test_board, True)
    