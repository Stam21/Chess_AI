import numpy as np
import ChessGame


matrix= [
            np.array(["bR","bN","bB","bQ","bK","bB","bN","bR"]),
            np.array(["bp","bp","bp","--","bp","bp","bp","bp"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["--","--","--","bp","--","--","--","--"]),
            np.array(["--","--","--","--","wp","--","--","--"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["wp","wp","wp","wp","--","wp","wp","wp"]),
            np.array(["wR","--","wB","wQ","wK","wB","wN","wR"])
        ]


VALUE_OF_ELEMENTS = {
    "--": 0,
    "p" : 1,
    "N" : 3,
    "B" : 3,
    "R" : 5,
    "Q" : 9,
    "K" : 1000,

    }

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

def convertToNumbers(elem):

    value = VALUE_OF_ELEMENTS[elem]

    return value


def utility_2_attacking(matrix, isWhite):
    blacks = 0
    whites = 0
    game_state = ChessGame.GameState()
    game_state.board=matrix
    game_state.blackKing = (0, 4)
    game_state.whiteKing = (7, 4)

    #section for the attacking
    array=[True, False]
    for elem in array:
        game_state.whiteMove=elem
        validMoves = game_state.getValidMoves()

        #for vm1 in validMovess:
         #   print(str(vm1.startRow) + "," + str(vm1.startCol))
         #   print(str(vm1.endRow) + "," + str(vm1.endCol))

        for vm in validMoves:
            if(matrix[vm.endRow][vm.endCol]!="--"):

                if(matrix[vm.startRow][vm.startCol][0]=="w" and matrix[vm.endRow][vm.endCol][0]=="b"):
                    whites=whites+int(VALUE_OF_ELEMENTS[matrix[vm.endRow][vm.endCol][1]])

                elif(matrix[vm.startRow][vm.startCol][0]=="b" and matrix[vm.endRow][vm.endCol][0]=="w"):

                    #print(str(vm.startRow) + "," + str(vm.startCol))
                    #print(str(vm.endRow) + "," + str(vm.endCol))
                    blacks=blacks+int(VALUE_OF_ELEMENTS[matrix[vm.endRow][vm.endCol][1]])
    #substract the player from machine color
    if(isWhite):
         return whites-blacks
    else:
        return blacks-whites

    #section for the protecting
def utility_2_protecting(matrix, isWhite):
    blacks = 0
    whites = 0
    game_state = ChessGame.GameState()
    game_state.board = matrix
    game_state.blackKing = (0, 4)
    game_state.whiteKing = (7, 4)

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
                print(matrix[x][y])
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
                for vm in game_state.moves:
                    if (matrix[vm.endRow][vm.endCol] != "--"):

                        if (matrix[vm.startRow][vm.startCol][0] == "w" and matrix[vm.endRow][vm.endCol][0] == "b"):
                            blacks = blacks + int(VALUE_OF_ELEMENTS[matrix[vm.endRow][vm.endCol][1]])
                        elif (matrix[vm.startRow][vm.startCol][0] == "b" and matrix[vm.endRow][vm.endCol][0] == "w"):
                            whites = whites + int(VALUE_OF_ELEMENTS[matrix[vm.endRow][vm.endCol][1]])

                matrix[x][y]=piece
    game_state.whiteMove=isWhite
    if (isWhite):
        return whites - blacks
    else:
        return blacks - whites


#isWhite true means the machine is white
isWhite=True
sum_attacking=utility_2_attacking(matrix, isWhite)
sum_protecting=utility_2_protecting(matrix, isWhite)
print(sum_protecting)
#combined_sum=sum_attacking+sum_protecting


