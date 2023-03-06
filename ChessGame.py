"""
This class stores all the information of the current state about the chess game, as well as 
information about the validity of moves.
"""
import numpy as np
import Actions
import chess

class GameState():
    def __init__(self):
        self.board = [
            np.array(["bR","bN","bB","bQ","bK","bB","bN","bR"]),
            np.array(["bp","bp","bp","bp","bp","bp","bp","bp"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["--","--","--","--","--","--","--","--"]),
            np.array(["wp","wp","wp","wp","wp","wp","wp","wp"]),
            np.array(["wR","wN","wB","wK","wQ","wB","wN","wR"])
        ]
        self.whiteMove = True
        self.blackKing = (0,4)
        self.whiteKing = (7,3)
        self.boardHelper = chess.Board( 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR')

    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol]= "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        if (move.pieceMoved == "wK"):
            self.whiteKing  = (move.endRow, move.endCol)
        elif (move.pieceMoved == "bK"):
            self.blackKing = (move.endRow, move.endCol)

        self.boardHelper.push(chess.Move.from_uci(move.getChessNotation()))
        self.whiteMove = not self.whiteMove 
        

    def getValidMoves(self):

        self.moves = []
        for move in self.boardHelper.legal_moves:
            self.moves.append(move)
        
        return self.moves
