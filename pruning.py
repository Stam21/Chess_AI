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
# Alpha-beta pruning used to optimize the minimax algorithm by reducenumber of nodes required to be evulated
#add two argument(alpha= best value by maximizing player, beta= best value for minimizing player)
def getNodeValue(board, isWhite, depth, alpha, beta, next_move, parent= None): 
    #terminal codition by depth
    if(depth == MAX_DEPTH):
        
        boardValue = W1*utility_1(board) + W2*utility_2(board) + W3*utility_3(board)
        return boardValue, next_move, parent
    
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
            return 0, next_move
        else:
            if (game_table.whiteMove == isWhite):
                return inf, next_move
            else:
                return -inf, next_move
            
        
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
            value = getNodeValue(child, isWhite, depth + 1, alpha, beta, False, parent=(nodeValue, child_index))[0]
            nodeValue = max(nodeValue, value)
            if nodeValue == value:
                next_move_idx = child_index
            # if the value > current 'nodeValue' then algorthim update'nodeValue'
            alpha = max(alpha, nodeValue) #algorthim also update 'alpha' to maxium its current value and 'nodeValue'
            if nodeValue >= beta:   
                # if 'v' >= 'beta', means the current node will delet, 
                # and algorithm prune the rest nodes in tree, this done by 'break'
                break
            child_index += 1

    else: #min's turn
        nodeValue = inf # turn 'nodeValue' into postive infinity
        for child in childrenNodes:  # goes deeper into the tree to get the values that come to this node
            value = getNodeValue(child, isWhite, depth + 1, alpha, beta, True, parent=(nodeValue, child_index))[0] #go through each child node
            nodeValue = min(nodeValue, value) #compute its value using recurisive call to 'getNode' above 
            if nodeValue == value:
                next_move_idx = child_index
            beta = min(beta, nodeValue)
            if nodeValue <= alpha:
                break
            child_index += 1
    print(alpha)
    print(beta)
    if depth == 0:
        next_move = moves[next_move_idx]

    return nodeValue, next_move, parent

def getNextMove(board, isWhite):
    next_move = "NOT YET CALCULATED"
    next_move = getNodeValue(board, isWhite, 0, inf, -inf, next_move)[1]
    return next_move
#####propagation##########

##########################
initialBoard = [[10,8,9,11,12,9,8,10],
                [7,7,7,7,7,7,7,7],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1],
                [4,2,3,5,6,3,2,4]]


print(getNextMove(initialBoard, True).getChessNotation())
