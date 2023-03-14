# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:00:04 2023

@author: Mario
"""
import numpy as np

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
    copy = matrix
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            copy[x][y] = NUMBERS_TO_STRINGS[matrix[x][y]]
        
        copy[x] = np.asarray(copy[x])
    
    return copy


    