# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:00:04 2023

@author: Mario
"""
import numpy as np
import copy

NUMBERS_TO_STRINGS = {
    0 : "--",
    1 : "wp",
    2 : "wN",
    3 : "wB",
    4 : "wR",
    5 : "wQ",
    6 : "wK",
    7 : "bp",
    8 : "bN",
    9 : "bB",
    10 : "bR",
    11 : "bQ",
    12 : "bK",
    
    }

def convertToStrings(matrix):
    mycopy = copy.deepcopy(matrix)
    for x in range(len(mycopy)):
        for y in range(len(mycopy[0])):
            mycopy[x][y] = NUMBERS_TO_STRINGS[mycopy[x][y]]
        
        mycopy[x] = np.asarray(mycopy[x])
    return mycopy
    