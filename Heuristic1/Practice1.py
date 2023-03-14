
board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
         ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
         ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
         ]

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
#calculate_board_value(board, 'White')
#calculate_board_value(board, 'Black')



