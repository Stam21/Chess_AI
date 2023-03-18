import random
from math import inf
import ChessGame
import adaptationBackboneToGUI as BtG
import copy

MAX_DEPTH = 3 #991 # if I go any hieger I get the "maximum recursion depth exceeded while calling a Python object" error
W1, W2, W3 = 0.6, 0.3, 0.1

####################MOCKS#######################

def utility_1(board):
    return 0.7

def utility_2(board):
    return -0.7

def utility_3(board):
    return 1
################################################

NUMBER = []
# Alpha-beta pruning used to optimize the minimax algorithm by reducenumber of nodes required to be evulated
#add two argument(alpha= best value by maximizing player, beta= best value for minimizing player)
def getNodeValue(board, isWhite, depth, alpha, beta, next_move):
    NUMBER.append(1)
    #terminal codition by depth
    if(depth == MAX_DEPTH):
        
        boardValue = W1*utility_1(board) + W2*utility_2(board) + W3*utility_3(board)
        return boardValue, next_move, alpha, beta
    
    game_table = ChessGame.GameState()
    str_board = BtG.convertToStrings(board) #convert board
    game_table.board = str_board
    if (depth%2 == 0): #max's turn
        game_table.whiteMove = isWhite
    else: #min's turn
        game_table.whiteMove = not isWhite
    
    moves = game_table.getValidMoves()
    
    #terminal condition by the rules
    if (len(moves) == 0):
        if (len(game_table.threats) == 0):
            return 0, next_move, alpha, beta
        else:
            if (game_table.whiteMove == isWhite):
                return inf, next_move, alpha, beta
            else:
                return -inf, next_move, alpha, beta
            
        
    #intermediate node
    childrenNodes = []
    for move in moves: #transform moves into states
        newBoard = copy.deepcopy(board)
        newBoard[move.startRow][move.startCol] = 0
        newBoard[move.endRow][move.endCol] = board[move.startRow][move.startCol]
        childrenNodes.append(newBoard)

    next_move_idx = 0
    child_index = 0
    if depth % 2 == 0:  #max's turn
        nodeValue = -inf #algorthim initializes 'nodeValue' to negative value, then next line:
        for child in childrenNodes:  
            # goes deeper into the tree to get the values that come to this node
            # goes thorugh every child node, compute its value in (recurisvely)call to 'getNodeValue'
            call = getNodeValue(child, isWhite, depth + 1, alpha, beta, False)
            value = call[0]
            alpha = max(call[3], alpha) #beta propagates up as alpha
            beta = min(call[2], alpha)  #alpha propagates up as beta
            nodeValue = max(nodeValue, value)
            if nodeValue == value:
                next_move_idx = child_index
            # if the value > current 'nodeValue' then algorthim update'nodeValue'
            alpha = max(alpha, nodeValue) #algorthim also update 'alpha' to maxium its current value and 'nodeValue'
            if nodeValue >= beta:
                print("betacut")
                # if 'v' >= 'beta', means the current node will delet, 
                # and algorithm prune the rest nodes in tree, this done by 'break'
                break
            child_index += 1

    else: #min's turn
        nodeValue = inf # turn 'nodeValue' into postive infinity
        for child in childrenNodes:  # goes deeper into the tree to get the values that come to this node 
            #go through each child node
            call = getNodeValue(child, isWhite, depth + 1, alpha, beta, True)
            value = call[0]
            alpha = max(call[3], alpha) #beta propagates up as alpha
            beta = min(call[2], alpha)  #alpha propagates up as beta
            nodeValue = min(nodeValue, value) #compute its value using recurisive call to 'getNode' above 
            if nodeValue == value:
                next_move_idx = child_index
            beta = min(beta, nodeValue)
            if nodeValue <= alpha:
                print("alfacut")
                break
            child_index += 1
    print("alpha:", alpha)
    print("beta:", beta)
    if depth == 0:
        next_move = moves[next_move_idx]

    return nodeValue, next_move, alpha, beta

def getNextMove(board, isWhite):
    next_move = "NOT YET CALCULATED"
    next_move = getNodeValue(board, isWhite, 0, -inf, inf, next_move)[1]
    return next_move

initialBoard = [[10,8,9,11,12,9,8,10],
                [7,7,7,7,7,7,7,7],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1],
                [4,2,3,5,6,3,2,4]]


print(getNextMove(initialBoard, True).getChessNotation())
