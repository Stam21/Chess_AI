
board = [[10,8,9,11,12,9,8,10],
         [7,7,7,7,7,7,7,7,],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [1,1,1,1,1,1,1,1],
         [4,2,3,5,6,3,2,4],
         ]
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


# define the point values for each piece type
piece_values = {
    'P': 1,  # Pawn
    'N': 3,  # Knight
    'B': 3,  # bishop
    'R': 5,  # rock
    'Q': 9,  # Queen
    'K': 10  # King(not counted)
}
# change the piece_types dictionary to map integers to their corresponding piece types as strings,
piece_types = {1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K'}


def count_board_value(board, color):
    value = 0
    piece_positions = {}
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row][col]
            if piece != "--":
                # Check if piece value is defined in dictionary
                piece_value = piece_values[piece_types[(piece[1])]]
                
                if piece [0] == 'w':
                    if color == 'White':
                        value += piece_value
                    else:
                        value -= piece_value
                else:
                    if color == 'Black':
                        value += piece_value
                    else:
                        value -= piece_value
                # Assign number to square
                square_num = row * 8 + col + 1
                # Add piece position to dictionary
                piece_positions[(row, col)] = piece_values.get(
                    piece_types[abs(piece)], 0)

                # Print out each piece's position and its value on the board
                piece_type = piece_types[abs(piece)]
                pos = f"{chr(col+65)}{8-row}"
                value = piece_values.get(piece_type, 0)
                print(f"{pos}:{piece_type}:{value}")
            else:
                # Assign number to square
                square_num = row * 8 + col + 1
                # Add empty square position and value to dictionary
                piece_positions[(row, col)] = 0

                # Print out empty square's position and its value on the board
                pos = f"{chr(col+65)}{8-row}"
            print(f"{pos}: :0")    

    return value, piece_positions
#count_board_value(board, 'White')
#count_board_value(board, 'Black')



