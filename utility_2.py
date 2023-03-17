import numpy as np
import ChessGame

#matrix for testing

matrix= [
            np.array(["bR","bN","bB","bQ","bK","bB","bN","bR"]),
            np.array(["bp","bp","bp","wp","wp","wp","bp","bp"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["wp","wp","wp","wp","wp","wp","wp","wp"]),
            np.array(["wR","wN","wB","wQ","wK","wB","wN","wR"])
        ]

#converting each pieces to the values they worth
VALUE_OF_ELEMENTS = {
    "--": 0,
    "p" : 1,
    "N" : 3,
    "B" : 3,
    "R" : 5,
    "Q" : 9,
    "K" : 1000,

    }

#function regarding converting each pieces to the values they worth
def convertToNumbers(elem):

    value = VALUE_OF_ELEMENTS[elem]

    return value

#attacking function part of the second utility function
def utility_2_attacking(matrix, isWhite):
    blacks = 0
    whites = 0
    game_state = ChessGame.GameState()
    game_state.board=matrix
    game_state.blackKing = (0, 4)
    game_state.whiteKing = (7, 4)

    #Array regarding changin the current move between the white and black teams
    Whitemove_array=[True, False]

    #Iterate through the whitemove array and get each time the valid moves
    for elem in Whitemove_array:
        game_state.whiteMove=elem
        validMoves = game_state.getValidMoves()

        #Go through each valid moves and append the value of the pieces that can be possible to eat from the opposite team
        for vm in validMoves:
            if(matrix[vm.endRow][vm.endCol]!="--"):

                if(matrix[vm.startRow][vm.startCol][0]=="w" and matrix[vm.endRow][vm.endCol][0]=="b"):

                    whites=whites+int(VALUE_OF_ELEMENTS[matrix[vm.endRow][vm.endCol][1]])

                elif(matrix[vm.startRow][vm.startCol][0]=="b" and matrix[vm.endRow][vm.endCol][0]=="w"):
                    blacks=blacks+int(VALUE_OF_ELEMENTS[matrix[vm.endRow][vm.endCol][1]])

    #substract the player from machine color
    if(isWhite):
         return (whites-blacks)/4000
    else:
        return (blacks-whites)/4000

#section for the protecting
def utility_2_protecting(matrix, isWhite):
    blacks = 0
    whites = 0
    game_state = ChessGame.GameState()
    game_state.board = matrix
    game_state.blackKing = (0, 4)
    game_state.whiteKing = (7, 4)

    #Iterate through the whole matrix and change each piece to the opposite colour
    #Then get the possible moves of the inverted piece
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y] != "--":
                piece = matrix[x][y]
                if piece[0] == 'b':
                    opponent = 'w'
                    game_state.whiteMove=True
                else:
                    opponent = 'b'
                    game_state.whiteMove = False
                matrix[x][y] = opponent + piece[1]
                threats=[]
                game_state.moves=[]
                if piece[1] == 'p':
                    game_state.getPawnMoves(x, y, threats)
                elif piece[1] == 'R':
                    game_state.getRookMoves(x, y, threats)
                elif piece[1] == 'N':
                    game_state.getKnightMoves(x, y, threats)
                elif piece[1] == 'B':
                    game_state.getBishopMoves(x, y, threats)
                elif piece[1] == 'K':
                    pass
                    #game_state.getKingMoves(x, y, threats, False)
                elif piece[1] == 'Q':
                    # Queen remaining and her moves are a combination of Rook and Bishop
                    game_state.getRookMoves(x, y, threats)
                    game_state.getBishopMoves(x, y, threats)

                #After getting the valid moves for the currently examined piece, the rest of the code sums up the protecting moves for eac colors
                for vm in game_state.moves:
                    if (matrix[vm.endRow][vm.endCol] != "--"):

                        if (matrix[vm.startRow][vm.startCol][0] == "w" and matrix[vm.endRow][vm.endCol][0] == "b"):
                            blacks = blacks + int(VALUE_OF_ELEMENTS[matrix[vm.endRow][vm.endCol][1]])
                        elif (matrix[vm.startRow][vm.startCol][0] == "b" and matrix[vm.endRow][vm.endCol][0] == "w"):
                            whites = whites + int(VALUE_OF_ELEMENTS[matrix[vm.endRow][vm.endCol][1]])

                matrix[x][y]=piece
    game_state.whiteMove=isWhite
    if (isWhite):
        return (whites - blacks)/4000
    else:
        return (blacks - whites)/4000


#isWhite true means the machine is white
isWhite=True

sum_attacking=utility_2_attacking(matrix, isWhite)
sum_protecting=utility_2_protecting(matrix, isWhite)
print(sum_attacking)
print(sum_protecting)
#combined_sum=sum_attacking+sum_protecting


