# Create the chess board(pawn=1, knight/bishop=3, rock=5, queen=9, empty square=0)
board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
         ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
         ]


# Create dictionary 'piece value'create numerical value for each tpye of piece 
piece_values = {
    'P': 1,  # Pawn
    'N': 3,  # Knight
    'B': 3,  # bishop
    'R': 5,  # rock
    'Q': 9,  # Queen
    'K': 10  # King()
}
# Variables are set to 0 or an empty dictionary to store total point value, and
# square number for each piece of the respective color.
white_points = 0
black_points = 0
white_square = {} # both empty dictionaries to store total points value
black_squares = {} # and square number of each piece of respective color

# define this function which takes 'board' and 'color' arguments, and it's return total
#points value of board for specific'color' 
def count_board_value(board, color):
    value = 0.    #initialize the function by assign it to 0
    piece_positions = {} # empty dictionary

#Through each element of board using two nest"For Loop".each element assigned to
#variable "piece" if not empyty, then fuction check its value is deined in
# 'piece_values' dict, if it define, then the value ssign to vairable, otherwise = 0
    for row in range(len(board)): # here we create a piece value for each row/col
        for col in range(len(board[row])):
            piece = board[row][col] ## assign piece values
            if piece != 0:
                # Check if piece value is defined in dictionary
                if piece in piece_values:
                    piece_value = piece_values[piece]
                else:
                    piece_value = 0
                if piece > 0:
                    if color == 'White':
                        value += piece_value
                    else:
                        value -= piece_value
                else:
                    if color == 'Black':
                        value += piece_value
                    else:
                        value -= piece_value
#it checks if piece belong  to specific color, and + or - the 'piece value' according to
#'value' and use the formula to defermine its color set up on its row & column index
                square_num_piece = row * 8 + col + 1
                if (row + col) % 2 == 0:
                    square_color = 'White'
                else:
                    square_color = 'Black'
                print(f"Suare{square_num_piece}({square_color}): {piece_value.get(piece,0)} ({piece_value})")
# Add piece position to dictionary
                piece_positions[(row, col)] = piece_values.get(piece, 0)
            else:
                square_num_piece= row * 8 + col + 1
                if (row + col) % 2 == 0:
                    square_color = 'White'
                else:
                    square_color = 'Black'
                print(f"Suare{square_num_piece}({square_color}): {0} (Empty)")    

#Function also add piece position to its value to "piece_position" dictionary
#and returns 'value' and 'piece position' as tuple.
    return value, piece_positions





## The output for the first square on chessboard(bR)is : Square1(black):5
## The output for empty on 4row and 3 col will be : Square 20(W): (Empty)
## Function count_board_Value will return the toal points of chessboard and the dictionary with 
#position and value of eacg piece on the board