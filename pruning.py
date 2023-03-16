import random
from math import inf
import ChessGame

MAX_DEPTH = 4

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
def getNodeValue(board, isWhite, depth, alpha, beta, next_move): 
 
    if depth == MAX_DEPTH:
        w1, w2, w3 = 0.6, 0.3, 0.1
        boardValue = w1 * utility_1(board) + w2 * utility_2(board) + w3 * utility_3(board)
        return boardValue, next_move

    # intermediate node
    game_table = ChessGame.GameState()
    game_table.board = board
    if depth % 2 == 0:  # turn into max
        game_table.whiteMove = isWhite
    else:  # turn into min
        game_table.whiteMove = not isWhite

    moves = game_table.getValidMoves()
    childrenNodes = []
    for move in moves:  # trans form moves into states
        newBoard = board
        newBoard[move.startRow][move.startCol] = 0
        newBoard[move.endRow][move.endCol] = board[move.startRow][move.startCol]
        childrenNodes.append(newBoard)

    if depth % 2 == 0:  
        nodeValue = -inf #algorthim initializes 'nodeValue' to negative value, then next line:
        for child in childrenNodes:  # goes deeper into the tree to get the values that come to this node
#go thorugh every child node, compute its value in (recurisvely)call to 'getNodeValue'
            
            value = getNodeValue(child, isWhite, depth - 1, alpha, beta, False)[0]
            nodeValue = max(nodeValue, value) 
# if the value > current 'nodeValue' then algorthim update'nodeValue'
            alpha = max(alpha, nodeValue) #algorthim also update 'alpha' to maxium its current value and 'nodeValue'
            if alpha >= beta:   #if 'alpha' >= to 'beta', means the current node will delet, 
                                #and algorithm prune the rest nodes in tree, this done by 'break'
                break
    else:  
        nodeValue = inf # turn 'nodeValue' into postive infinity
        for child in childrenNodes:  # goes deeper into the tree to get the values that come to this node
            value = getNodeValue(child, isWhite, depth - 1, alpha, beta, True)[0] #go through each child node
            nodeValue = min(nodeValue, value) #compute its value using recurisive call to 'getNode' above 
            beta = min(beta, nodeValue)
            if beta <= alpha:
                break

    if depth == 0:
        idx = nodeValue.index(max(nodeValue))
        next_move = moves[idx]

    return nodeValue, next_move

