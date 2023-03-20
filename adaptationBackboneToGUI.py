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
    12 : "bK"

    }

STRINGS_TO_NUMBERS = {
    "--" : 0,
    "wp" : 1,
    "wN" : 2,
    "wB" : 3,
    "wR" : 4,
    "wQ" : 5,
    "wK" : 6,
    "bp" : 7,
    "bN" : 8,
    "bB" : 9,
    "bR" : 10,
    "bQ" : 11,
    "bK" : 12
    }

def convertToStrings(matrix):
    mycopy = copy.deepcopy(matrix)
    for x in range(len(mycopy)):
        for y in range(len(mycopy[0])):
            mycopy[x][y] = NUMBERS_TO_STRINGS[mycopy[x][y]]

        mycopy[x] = np.asarray(mycopy[x])
    return mycopy

def convertToNumbers(matrix):
    mycopy = copy.deepcopy(matrix)
    for x in range(len(mycopy)):
        mycopy[x] = mycopy[x].tolist()
        for y in range(len(mycopy[0])):
            mycopy[x][y] = int(STRINGS_TO_NUMBERS[mycopy[x][y]])
    return mycopy