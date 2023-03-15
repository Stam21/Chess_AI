import adaptationBackboneToGUI as adap
import numpy as np

board = [[10,8,9,11,12,9,8,10],
         [7,7,7,7,7,7,7,7],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [1,1,1,1,1,1,1,1],
         [4,2,3,5,6,3,2,4],
         ]

# Create dictionary 'piece value'create numerical value for each tpye of piece 
piece_values = {
    1 : 1,  # Pawn
    2 : 3,  # Knight
    3 : 3,  # bishop
    4 : 5,  # rock
    5 : 9,  # Queen
    0 : 10  # King()
}
# Variables are set to 0 or an empty dictionary to store total point value, and
# square number for each piece of the respective color.
white_points = 0
black_points = 0
white_square = {} # both empty dictionaries to store total points value
black_squares = {} # and square number of each piece of respective color

#define this function which takes 'board' and 'color' arguments, and it's return total
#points value of board for specific'color' 
def count_board_value(board,color):
    
    value = 0    #initialize the function by assign it to 0
 
#Through each element of board using two nest"For Loop".each element assigned to
#variable "piece" if not empyty, then fuction check its value is deined in
# 'piece_values' dict, if it define, then the value ssign to vairable, otherwise = 0
    for row in range(len(board)): # here we create a piece value for each row/col
        for col in range(len(board[row])):
            piece = board[row][col] 
            if piece != 0:
                if color and int((piece-1)/6) == 0 or not color and int((piece-1)/6) == 1:
                
                     value += piece_values[piece%6]
                else:
                    value -= piece_values[piece%6]
    print(value)                
    return value / 49
count_board_value(board,True) #for White         
#count_board_value(board,False) for 'Black'

