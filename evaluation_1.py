
test_board = [[10,8,9,11,12,9,8,10],
         [7,7,7,7,7,7,7,7],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [1,1,1,1,1,1,1,1],
         [4,2,3,5,6,3,2,4],
         ]

# Create dictionary 'piece value'create numerical value for each tpye of piece 
PIECE_VALUES = {
    1 : 1,  # Pawn
    2 : 3,  # Knight
    3 : 3,  # bishop
    4 : 5,  # rock
    5 : 9,  # Queen
    6 : 100  # King()
}

#define this function which takes 'board' and 'color' arguments, and it's return total
#points value of board for specific'color' 
def evaluation_1(board,color):
    value = 0    #initialize the function by assign it to 0
#Through each element of board using two nest"For Loop".each element assigned to
#variable "piece" if not empyty, then fuction check its value is deined in
# 'piece_values' dict, if it define, then the value ssign to vairable, otherwise = 0
    for row in range(len(board)): # here we create a piece value for each row/col
        for col in range(len(board[row])):
            piece = board[row][col] 
            if piece != 0:
                if (piece/6 <= 1):
                     value += PIECE_VALUES[piece]
                elif (piece/6 > 1):
                    value -= PIECE_VALUES[piece-6] 
                          
    return value/49
#evaluation_1(test_board,True) #for White         
#evaluation_1(test_board,False) for 'Black'

