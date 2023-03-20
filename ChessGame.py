"""
This class stores all the information of the current state about the chess game, as well as 
information about the validity of moves.
"""
import numpy as np
import math
import Actions

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
            np.array(["wR","wN","wB","wQ","wK","wB","wN","wR"])
        ]
        self.whiteMove = True
        # Initial position of kings.
        self.whiteKing = ()
        self.blackKing = ()
        self.threats = []
        self.moves=[]
        self.pins=[]
        self.potentialThreats = []
        #Store state of pawn promotion
        self.whitePawnsPromo = False
        self.blackPawnsPromo = False
        #Store state of move for each pawn so en passant can be applied
        self.whitePawns = [False,False,False,False,False,False,False,False]
        self.blackPawns = [False,False,False,False,False,False,False,False]
        #First value represents queenside castling and second value kingside
        self.castleWhite = [False,False] 
        self.castleBlack = [False,False]

    def makeMove(self, move):
        '''
        Function that makes the change in the board when a move is confirmed.
        '''
        if (move.pieceMoved == "wK"):
            # If the move is to castle make appropriate changes to the board.
            if (move.endRow == 7 and move.endCol == 2 and not self.castleWhite[0]):
                self.board[move.startRow][move.endCol+1]= "wR"
                self.board[7][0] = "--"
            elif (move.endRow == 7 and move.endCol == 6 and not self.castleWhite[1]):
                self.board[move.startRow][move.endCol-1]= "wR"
                self.board[7][7] = "--"
            # Change the position of the king.
            self.whiteKing  = (move.endRow, move.endCol)
            # King is moved so castling is not applicable from now on.
            self.castleWhite = [True,True]
        elif (move.pieceMoved == "bK"):
            if (move.endRow == 0 and move.endCol == 2 and not self.castleBlack[0]):
                self.board[move.startRow][move.endCol+1]= "bR"
                self.board[0][0] = "--"
            elif (move.endRow == 0 and move.endCol == 6 and not self.castleBlack[1]):
                self.board[move.startRow][move.endCol-1]= "bR"
                self.board[0][7] = "--"
            self.blackKing = (move.endRow, move.endCol)
            self.castleBlack = [True,True]
        elif (move.pieceMoved == "wR" and (move.startCol == 0 or move.startCol == 7)):
            # Depending on the rook that was moved make inapplicable the castling on queen side or king side.
            if (move.startCol == 0):
                self.castleWhite[0] = True
            else: 
                self.castleWhite[1] = True
        elif (move.pieceMoved == "bR" and (move.startCol == 0 or move.startCol == 7)):
            if (move.startCol == 0):
                self.castleBlack[0] = True
            else: 
                self.castleBlack[1] = True       
        elif (move.pieceMoved == "wp" ):
                if (not(move.startRow == 6 and (abs(move.startRow - move.endRow) == 2))):
                        self.whitePawns[move.startCol] = True 
                if ( self.board[move.endRow+1][move.endCol]== "bp" and not self.blackPawns[move.startCol]):
                    self.board[move.endRow+1][move.endCol]= "--"
                if (move.endRow == 0):
                    self.whitePawnsPromo = True
        elif (move.pieceMoved == "bp"):
                if (not(move.startRow == 1 and (abs(move.startRow - move.endRow) == 2))):
                        self.blackPawns[move.startCol] = True
                if (self.board[move.endRow-1][move.endCol]== "wp" and not self.whitePawns[move.startCol]):
                    self.board[move.endRow-1][move.endCol]= "--"
                if (move.endRow == len(self.board)-1):
                    self.blackPawnsPromo = True

        for y in range(8):
            if (self.board[6][y] == "--"):
                self.whitePawns[y] = True
            if (self.board[1][y] == "--"):
                self.blackPawns[y] = True

        self.board[move.startRow][move.startCol]= "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved

        self.movesHistory = [] # Moves history can be used to roll back to previous moves
        self.whiteMove = not self.whiteMove # Change player
        

    def getValidMoves(self):
        '''
        Returns a list of Actions.Move objects with the valid moves for current player.
        '''
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if (self.board[x][y]=="bK"):
                    self.blackKing = (x,y)
                if (self.board[x][y]=="wK"):
                    self.whiteKing = (x,y)
        self.whitePawnsPromo = False # Pawn promotion state should be reset when player is switched because it affects the validity of moves.
        self.blackPawnsPromo = False
        threats = self.getChecked()
        self.threats = threats
        self.moves = []
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                player = self.board[x][y][0]
                if ((player=='w' and self.whiteMove) or (player=='b' and not self.whiteMove)):
                    piece  = self.board[x][y][1]
                    if piece == 'p':
                        self.getPawnMoves(x,y,threats)
                    elif piece =='R':
                        self.getRookMoves(x,y,threats)
                    elif piece == 'N':
                        self.getKnightMoves(x,y,threats)
                    elif piece == 'B':
                        self.getBishopMoves(x,y,threats)
                    elif piece == 'K':
                        self.getKingMoves(x,y,threats,False)
                    elif piece == 'Q':
                        #Queen remaining and her moves are a combination of Rook and Bishop
                        self.getRookMoves(x,y,threats)
                        self.getBishopMoves(x,y,threats)
        return self.moves
    
    def getPawnMoves(self,x,y,threats):
        '''
        Function to append all valid moves for the pawn.
        '''
        if self.whiteMove:
            #move pawn 1 square ahead
            if ((self.board[x-1][y] == "--") and (self.calculateLine(x-1,y,threats,self.whiteKing) and (self.findPins(x,y,self.pins) or self.calculateLine(x-1,y,self.potentialThreats,self.whiteKing)))):
                self.moves.append(Actions.Move((x,y),(x-1,y),self.board))
                #move pawn 2 squares ahead
                if ((x==6 and self.board[x-2][y] == "--") and (self.calculateLine(x-2,y,threats,self.whiteKing) and (self.findPins(x,y,self.pins) or self.calculateLine(x-1,y,self.potentialThreats,self.whiteKing)))):
                    self.moves.append(Actions.Move((x,y),(x-2,y),self.board))
            #move pawn 1 square ahead and left or right if there is an enemy piece.
            if (y > 0):
                if (self.board[x-1][y-1][0] == 'b' and (self.calculateLine(x-1,y-1,threats,self.whiteKing) and (self.findPins(x,y,self.pins) or self.board[x-1][y-1] == "bQ" or self.board[x-1][y-1] == "bB" ))):
                    self.moves.append(Actions.Move((x,y),(x-1,y-1),self.board))
                    
            if (y < len(self.board)-1):
                if (self.board[x-1][y+1][0] == 'b' and (self.calculateLine(x-1,y+1,threats,self.whiteKing) and (self.findPins(x,y,self.pins) or self.board[x-1][y+1] == "bQ" or self.board[x-1][y+1] == "bB" ))):
                    self.moves.append(Actions.Move((x,y),(x-1,y+1),self.board))
                    
            #en passant
            if (x > 0 and y <len(self.board)-1 and y>0):
                if ((self.board[x][y-1] == "bp") and not self.blackPawns[y-1]):
                    self.moves.append(Actions.Move((x,y),(x-1,y-1),self.board))
                elif ((self.board[x][y+1] == "bp") and not self.blackPawns[y+1]):
                    self.moves.append(Actions.Move((x,y),(x-1,y+1),self.board))
            

        else:
            #move pawn 1 square ahead
            if ((self.board[x+1][y] == "--") and self.calculateLine(x+1,y,threats,self.blackKing) and (self.findPins(x,y,self.pins) or self.calculateLine(x-1,y,self.potentialThreats,self.blackKing) )):
                self.moves.append(Actions.Move((x,y),(x+1,y),self.board))
                #move pawn 2 squares ahead
                if ((x==1 and self.board[x+2][y] == "--") and self.calculateLine(x+2,y,threats,self.blackKing) and (self.findPins(x,y,self.pins) or self.calculateLine(x-1,y,self.potentialThreats,self.blackKing))):
                    self.moves.append(Actions.Move((x,y),(x+2,y),self.board))
            #move pawn 1 square ahead and left or right if there is an enemy piece.
            if (y > 1):    
                if (self.board[x+1][y-1][0] == 'w' and self.calculateLine(x+1,y-1,threats,self.blackKing) and (self.findPins(x,y,self.pins) or self.board[x+1][y-1] == "wQ" or self.board[x+1][y-1] == "wB")):
                    self.moves.append(Actions.Move((x,y),(x+1,y-1),self.board))
            if (y < len(self.board)-1):    
                if (self.board[x+1][y+1][0] == 'w' and self.calculateLine(x+1,y+1,threats,self.blackKing) and (self.findPins(x,y,self.pins) or self.board[x+1][y+1] == "wQ" or self.board[x+1][y+1] == "wB")):
                    self.moves.append(Actions.Move((x,y),(x+1,y+1),self.board))
            #en passant
            if (x < 6 and y <len(self.board)-1 and y>0):
                if ((self.board[x][y-1] == "wp") and not self.whitePawns[y-1]):
                    self.moves.append(Actions.Move((x,y),(x+1,y-1),self.board))
                elif ((self.board[x][y+1] == "wp") and not self.whitePawns[y+1]):
                    self.moves.append(Actions.Move((x,y),(x+1,y+1),self.board))


    def getRookMoves(self,x,y,threats):
        '''
        Function to append all valid moves for the rook.
        '''
        if self.whiteMove:
            player = 'w'
            opponent = 'b'
            pos_King = self.whiteKing
        else:
            player = 'b'
            opponent = 'w'
            pos_King = self.blackKing

        #move rook right-left-up-down squares, flags indicate if an obstacle was met in a direction.
        counter = 1
        flagE = False
        flagW = False
        flagN = False
        flagS = False
        while (not (flagE and flagW and flagN and flagS)):
                if  (x - counter >= 0 and (not flagW)):
                    if (self.board[x-counter][y] == "--" or self.board[x-counter][y][0] == opponent) and self.calculateLine(x-counter,y,threats,pos_King) and (self.findPins(x,y,self.pins)) :
                            self.moves.append(Actions.Move((x,y),(x-counter,y),self.board))
                            if (self.board[x-counter][y][0] == opponent):
                                flagW = True
                    elif (self.board[x-counter][y] == "--" or self.board[x-counter][y][0] == opponent) and self.calculateLine(x-counter,y,threats,pos_King): 
                            for threat in threats:    
                                if (x-counter == threat[0] and y == threat[1]) or self.calculateLine(x,y,[threat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x-counter,y),self.board))
                            for pthreat in self.potentialThreats:
                                if (x-counter == pthreat[0] and y == pthreat[1]) or self.calculateLine(x,y,[pthreat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x-counter,y),self.board))
                            if self.calculateLine(x-counter,y,self.potentialThreats,pos_King) and not self.calculateLine(x,y,self.potentialThreats,pos_King):
                                    self.moves.append(Actions.Move((x,y),(x-counter,y),self.board))
                            if (self.board[x-counter][y][0] == opponent):
                                flagW = True
                    elif (self.board[x-counter][y][0] == player):
                        flagW = True
                    
                else:
                    flagW = True
                if  (y - counter >= 0 and (not flagN)):
                    if (self.board[x][y-counter] == "--" or self.board[x][y-counter][0] == opponent) and self.calculateLine(x,y-counter,threats,pos_King) and (self.findPins(x,y,self.pins)) :
                            self.moves.append(Actions.Move((x,y),(x,y-counter),self.board))
                            if (self.board[x][y-counter][0] == opponent):
                                flagN = True
                    elif (self.board[x][y-counter] == "--" or self.board[x][y-counter][0] == opponent) and self.calculateLine(x,y-counter,threats,pos_King):
                            for threat in threats:    
                                if (x == threat[0] and y-counter == threat[1]) or self.calculateLine(x,y,[threat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x,y-counter),self.board))
                            for pthreat in self.potentialThreats:
                                if (x == pthreat[0] and y-counter == pthreat[1]) or self.calculateLine(x,y,[pthreat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x,y-counter),self.board))
                            if self.calculateLine(x,y-counter,self.potentialThreats,pos_King) and not self.calculateLine(x,y,self.potentialThreats,pos_King):
                                self.moves.append(Actions.Move((x,y),(x,y-counter),self.board))
                            if (self.board[x][y-counter][0] == opponent):
                                flagN = True
                    elif (self.board[x][y-counter][0] == player):
                        flagN = True
                    
                else:
                    flagN = True
                if  (y + counter < len(self.board) and (not flagS)):
                    if (self.board[x][y+counter] == "--" or self.board[x][y+counter][0] == opponent) and self.calculateLine(x,y+counter,threats,pos_King) and (self.findPins(x,y,self.pins)) :
                            self.moves.append(Actions.Move((x,y),(x,y+counter),self.board))
                            if (self.board[x][y+counter][0] == opponent):
                                flagS = True
                    elif (self.board[x][y+counter] == "--" or self.board[x][y+counter][0] == opponent) and self.calculateLine(x,y+counter,threats,pos_King): 
                            for threat in threats:
                                if  (x == threat[0] and y+counter == threat[1]) or self.calculateLine(x,y,[threat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x,y+counter),self.board))
                            for pthreat in self.potentialThreats:
                                if (x == pthreat[0] and y+counter == pthreat[1]) or self.calculateLine(x,y,[pthreat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x,y+counter),self.board))
                            if self.calculateLine(x,y+counter,self.potentialThreats,pos_King) and not self.calculateLine(x,y,self.potentialThreats,pos_King):
                                self.moves.append(Actions.Move((x,y),(x,y+counter),self.board))
                            if (self.board[x][y+counter][0] == opponent):
                                flagS = True
                    elif (self.board[x][y+counter][0] == player):
                        flagS = True
                else:
                    flagS = True
                if (x + counter < len(self.board) and (not flagE)):
                    if (self.board[x+counter][y] == "--" or self.board[x+counter][y][0] == opponent) and self.calculateLine(x+counter,y,threats,pos_King) and (self.findPins(x,y,self.pins)) :
                            self.moves.append(Actions.Move((x,y),(x+counter,y),self.board))
                            if (self.board[x+counter][y][0] == opponent):
                                flagE = True
                    elif (self.board[x+counter][y] == "--" or self.board[x+counter][y][0] == opponent) and self.calculateLine(x+counter,y,threats,pos_King): 
                            for threat in threats:
                                if (x+counter == threat[0] and y == threat[1]) or self.calculateLine(x,y,[threat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x+counter,y),self.board))
                            for pthreat in self.potentialThreats:
                                if (x+counter == pthreat[0] and y == pthreat[1]) or self.calculateLine(x,y,[pthreat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x+counter,y),self.board))
                            if self.calculateLine(x+counter,y,self.potentialThreats,pos_King) and not self.calculateLine(x,y,self.potentialThreats,pos_King):
                                self.moves.append(Actions.Move((x,y),(x+counter,y),self.board))
                            if (self.board[x+counter][y][0] == opponent):
                                flagE = True
                    elif (self.board[x+counter][y][0] == player):
                        flagE = True
                else:
                    flagE = True

                counter +=1


    def getKnightMoves(self,x,y,threats):
        '''
        Function to append all valid moves for the knight.
        '''
        if self.whiteMove:
            opponent = 'b'
            pos_King = self.whiteKing
        else:
            opponent = 'w'
            pos_King = self.blackKing

        if (x - 2 >= 0):
            if (y-1 >=0):
                if (self.board[x-2][y-1] == "--" or self.board[x-2][y-1][0] == opponent) and self.calculateLine(x-2,y-1,threats,pos_King) and (self.findPins(x,y,self.pins)):
                    self.moves.append(Actions.Move((x,y),(x-2,y-1),self.board))
            if (y+1 < len(self.board)):
                if (self.board[x-2][y+1] == "--" or self.board[x-2][y+1][0] == opponent) and self.calculateLine(x-2,y+1,threats,pos_King) and (self.findPins(x,y,self.pins)):
                    self.moves.append(Actions.Move((x,y),(x-2,y+1),self.board))
        if (y - 2 >= 0):
            if (x-1 >=0):
                if (self.board[x-1][y-2] == "--" or self.board[x-1][y-2][0] == opponent) and self.calculateLine(x-1,y-2,threats,pos_King) and (self.findPins(x,y,self.pins)):
                    self.moves.append(Actions.Move((x,y),(x-1,y-2),self.board))
            if (x+1 < len(self.board)):
                if (self.board[x+1][y-2] == "--" or self.board[x+1][y-2][0] == opponent) and self.calculateLine(x+1,y-2,threats,pos_King) and (self.findPins(x,y,self.pins)):
                    self.moves.append(Actions.Move((x,y),(x+1,y-2),self.board))

        if  (y + 2 < len(self.board)):
            if (x-1 >=0):
                if (self.board[x-1][y+2] == "--" or self.board[x-1][y+2][0] == opponent) and self.calculateLine(x-1,y+2,threats,pos_King) and (self.findPins(x,y,self.pins)):
                    self.moves.append(Actions.Move((x,y),(x-1,y+2),self.board))
            if (x+1 < len(self.board)):
                if (self.board[x+1][y+2] == "--" or self.board[x+1][y+2][0] == opponent) and self.calculateLine(x+1,y+2,threats,pos_King) and (self.findPins(x,y,self.pins)):
                    self.moves.append(Actions.Move((x,y),(x+1,y+2),self.board))

        if (x + 2 < len(self.board)):
            if (y-1 >=0):
                if (self.board[x+2][y-1] == "--" or self.board[x+2][y-1][0] == opponent) and self.calculateLine(x+2,y-1,threats,pos_King) and (self.findPins(x,y,self.pins)):
                    self.moves.append(Actions.Move((x,y),(x+2,y-1),self.board))
            if (y+1 < len(self.board)):
                if (self.board[x+2][y+1] == "--" or self.board[x+2][y+1][0] == opponent) and self.calculateLine(x+2,y+1,threats,pos_King) and (self.findPins(x,y,self.pins)):
                    self.moves.append(Actions.Move((x,y),(x+2,y+1),self.board))

    def getBishopMoves(self,x,y,threats):

        '''
        Function to append all valid moves for the bishop.
        '''

        if self.whiteMove:
            opponent = 'b'
            player = 'w'
            pos_King = self.whiteKing
        else:
            player = 'b'
            opponent = 'w'
            pos_King = self.blackKing

        counter = 1
        # Flags to track whether an obstacle is met in each of the directions.
        flagNE = False
        flagNW = False
        flagSE = False
        flagSW = False

        '''
        x-counter and y-counter means North-West diagonal
        x-counter and y+counter means South-West diagonal
        x+counter and y-counter means North-East diagonal
        x+counter and y+counter means South-East diagonal
        '''
        while (not (flagNE and flagSE and flagNW and flagSW)):
                if (x - counter >= 0 and y-counter >= 0 and (not flagNW)):
                    if (self.board[x-counter][y-counter] == "--" or self.board[x-counter][y-counter][0] == opponent) and self.calculateLine(x-counter,y-counter,threats,pos_King) and (self.findPins(x,y,self.pins)) :
                            self.moves.append(Actions.Move((x,y),(x-counter,y-counter),self.board))
                            if (self.board[x-counter][y-counter][0] == opponent):
                                flagNW = True
                    elif (self.board[x-counter][y-counter] == "--" or self.board[x-counter][y-counter][0] == opponent) and self.calculateLine(x-counter,y-counter,threats,pos_King):
                            for threat in threats:
                                if (x-counter == threat[0] and y-counter == threat[1]) or self.calculateLine(x,y,[threat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x-counter,y-counter),self.board))
                            for pthreat in self.potentialThreats:
                                if (x-counter == pthreat[0] and y-counter == pthreat[1]) or self.calculateLine(x,y,[pthreat],pos_King):
                                    self.moves.append(Actions.Move((x,y),(x-counter,y-counter),self.board))
                            if self.calculateLine(x-counter,y-counter,self.potentialThreats,pos_King) and not self.calculateLine(x,y,self.potentialThreats,pos_King):
                                self.moves.append(Actions.Move((x,y),(x-counter,y-counter),self.board))
                            if (self.board[x-counter][y-counter][0] == opponent):
                                    flagNW = True
                    elif (self.board[x-counter][y-counter][0] == player):
                        flagNW = True
                else:
                    flagNW = True
                if (x - counter >= 0 and y + counter < len(self.board) and (not flagSW)):
                    if (self.board[x-counter][y+counter] == "--" or self.board[x-counter][y+counter][0] == opponent) and self.calculateLine(x-counter,y+counter,threats,pos_King) and (self.findPins(x,y,self.pins)):
                        self.moves.append(Actions.Move((x,y),(x-counter,y+counter),self.board))
                        if (self.board[x-counter][y+counter][0] == opponent):
                                flagSW = True
                    elif (self.board[x-counter][y+counter] == "--" or self.board[x-counter][y+counter][0] == opponent) and self.calculateLine(x-counter,y+counter,threats,pos_King):
                        for threat in threats:
                            if (x-counter == threat[0] and y+counter == threat[1]) or self.calculateLine(x,y,[threat],pos_King):    
                                self.moves.append(Actions.Move((x,y),(x-counter,y+counter),self.board))
                        for pthreat in self.potentialThreats:
                            if (x-counter == pthreat[0] and y+counter == pthreat[1]) or self.calculateLine(x,y,[pthreat],pos_King):
                                self.moves.append(Actions.Move((x,y),(x-counter,y+counter),self.board))
                        if self.calculateLine(x-counter,y+counter,self.potentialThreats,pos_King) and not self.calculateLine(x,y,self.potentialThreats,pos_King):
                                self.moves.append(Actions.Move((x,y),(x-counter,y+counter),self.board))
                        if (self.board[x-counter][y+counter][0] == opponent):
                            flagSW = True
                    elif (self.board[x-counter][y+counter][0] == player):
                        flagSW = True
                else:
                    flagSW = True
                if (x + counter < len(self.board) and y - counter >=0 and (not flagNE)):
                    if (self.board[x+counter][y-counter] == "--" or self.board[x+counter][y-counter][0] == opponent) and self.calculateLine(x+counter,y-counter,threats,pos_King) and (self.findPins(x,y,self.pins)):
                        self.moves.append(Actions.Move((x,y),(x+counter,y-counter),self.board))
                        if (self.board[x+counter][y-counter][0] == opponent):
                                flagNE = True
                    elif (self.board[x+counter][y-counter] == "--" or self.board[x+counter][y-counter][0] == opponent) and self.calculateLine(x+counter,y-counter,threats,pos_King):
                        for threat in threats:    
                            if (x+counter == threat[0] and y-counter == threat[1]) or self.calculateLine(x,y,[threat],pos_King):
                                self.moves.append(Actions.Move((x,y),(x+counter,y-counter),self.board))
                        for pthreat in self.potentialThreats:
                            if (x+counter == pthreat[0] and y-counter == pthreat[1]) or self.calculateLine(x,y,[pthreat],pos_King):
                                self.moves.append(Actions.Move((x,y),(x+counter,y-counter),self.board))
                        if self.calculateLine(x+counter,y-counter,self.potentialThreats,pos_King) and not self.calculateLine(x,y,self.potentialThreats,pos_King):
                                self.moves.append(Actions.Move((x,y),(x+counter,y-counter),self.board))
                        if (self.board[x+counter][y-counter][0] == opponent):
                            flagNE = True
                    elif (self.board[x+counter][y-counter][0] == player):
                        flagNE = True
                else:
                    flagNE = True
                if (x + counter < len(self.board) and y + counter < len(self.board) and (not flagSE)):
                    if (self.board[x+counter][y+counter] == "--" or self.board[x+counter][y+counter][0] == opponent) and self.calculateLine(x+counter,y+counter,threats,pos_King) and (self.findPins(x,y,self.pins)):
                        self.moves.append(Actions.Move((x,y),(x+counter,y+counter),self.board))
                        if (self.board[x+counter][y+counter][0] == opponent):
                                flagSE = True
                    elif (self.board[x+counter][y+counter] == "--" or self.board[x+counter][y+counter][0] == opponent) and self.calculateLine(x+counter,y+counter,threats,pos_King):
                        for threat in threats:
                            if (x+counter == threat[0] and y+counter == threat[1]) or self.calculateLine(x,y,[threat],pos_King):
                                self.moves.append(Actions.Move((x,y),(x+counter,y+counter),self.board))
                        for pthreat in self.potentialThreats:
                            if (x+counter == pthreat[0] and y+counter == pthreat[1]) or self.calculateLine(x,y,[pthreat],pos_King):
                                self.moves.append(Actions.Move((x,y),(x+counter,y+counter),self.board))
                        if self.calculateLine(x+counter,y+counter,self.potentialThreats,pos_King) and not self.calculateLine(x,y,self.potentialThreats,pos_King):
                                self.moves.append(Actions.Move((x,y),(x+counter,y+counter),self.board))
                        if (self.board[x+counter][y+counter][0] == opponent):
                            flagSE = True
                    elif (self.board[x+counter][y+counter][0] == player):
                        flagSE = True
                else:
                    flagSE = True

                counter +=1
    def getKingMoves(self,x,y,threats,recursion):
        '''
        Function to append all valid moves for the king.
        '''
        if self.whiteMove:
            opponent = 'b'
            # Check if it is feasible for the white king to castle and if so add this move to valid moves.
            if (self.whiteKing == (7,4) and self.board[7][0] == "wR" and self.checkCastling(7,4,0,self.castleWhite) and len(threats)==0):
                self.moves.append(Actions.Move((7,4),(7,2),self.board))
            elif (self.whiteKing == (7,4) and self.board[7][7] == "wR" and self.checkCastling(7,4,7,self.castleWhite) and len(threats)==0):
                self.moves.append(Actions.Move((7,4),(7,6),self.board))
        else:
            opponent = 'w'
            if (self.blackKing == (0,4) and self.board[0][0] == "bR" and self.checkCastling(0,4,0,self.castleBlack) and len(threats)==0):
                self.moves.append(Actions.Move((0,4),(0,2),self.board))
            elif (self.blackKing == (0,4) and self.board[0][7] == "bR" and self.checkCastling(0,4,7,self.castleBlack) and len(threats)==0):
                self.moves.append(Actions.Move((0,4),(0,6),self.board))
        

        moves = self.moves

        # Valid moves for the king are only the neighbouring squares.
        for square_x in range(-1,2):
            for square_y in range(-1,2):
                if (not (square_x == 0 and square_y == 0) and (y+square_y>=0 and y+square_y<len(self.board) and x+square_x>=0 and x+square_x<len(self.board))):
                    if (self.board[x+square_x][y+square_y] == "--" or self.board[x+square_x][y+square_y][0] == opponent):
                        threatstmp = []
                        # Store all the points with direct attacks to the king
                        if (not recursion):
                            # This if statement is only used for the current position of the king.
                            # For every possible next move of the king find all threats and if a threat exists, this move is not valid. 
                            self.moves = []
                            self.getRookMoves(x+square_x,y+square_y,[])
                            self.getBishopMoves(x+square_x,y+square_y,[])
                            for move in self.moves:
                                if(self.board[move.endRow][move.endCol][1] == 'Q'):
                                    threatstmp.append((move.endRow,move.endCol))
                                elif(self.board[move.endRow][move.endCol][1] == 'B' and (x+square_x!=move.endRow and y+square_y!=move.endCol)):
                                    threatstmp.append((move.endRow,move.endCol))
                                elif(self.board[move.endRow][move.endCol][1] == 'R' and (x+square_x==move.endRow or y+square_y==move.endCol)):
                                    threatstmp.append((move.endRow,move.endCol))
                            
                            self.moves = []
                            self.getKnightMoves(x+square_x,y+square_y,[])
                            for move in self.moves:
                                if(self.board[move.endRow][move.endCol][1] == 'N'):
                                    threatstmp.append((move.endRow,move.endCol))
                            
                            self.moves = []
                            self.getPawnMoves(x+square_x,y+square_y,[])
                            for move in self.moves:
                                if(self.board[move.endRow][move.endCol][1] == 'p'):
                                    threatstmp.append((move.endRow,move.endCol)) 
                        
                            self.moves = []
                            self.getKingMoves(x+square_x,y+square_y,[],True)
                            for move in self.moves:
                                if(self.board[move.endRow][move.endCol][1] == 'K'):
                                    threatstmp.append((move.endRow,move.endCol)) 

                        if (len(threatstmp) + len(threats)) == 0 or (self.board[x+square_x][y+square_y][0] == opponent and \
                            (self.calculateLine(x+square_x,y+square_y,threatstmp,(x,y)))) or \
                            (not self.calculateLine(x+square_x,y+square_y,threats,(x,y)) and (self.calculateLine(x+square_x,y+square_y,threatstmp,(x,y)))):
                            moves.append(Actions.Move((x,y),(x+square_x,y+square_y),self.board))

        
        self.moves = moves
    

    def getChecked(self):
        ''' 
        Check for direct threats to the king or checks and for possible threats or pins.
        Threats or Checks to the king are stored in the threats list.
        Possible threats or Pins to the king are stored in the pins list.
        '''
        if (self.whiteMove):
            king_pos = self.whiteKing

        else:
            king_pos = self.blackKing

        self.moves = []
        self.pins = []
        self.potentialThreats = []
        threats = []
        self.getRookMoves(king_pos[0],king_pos[1],[])
        self.getBishopMoves(king_pos[0],king_pos[1],[])

        # Store all the points with direct attacks to the king
        # Use all possible moves with the kings' coordinates to get the attacks
        for move in self.moves:
            if(self.board[move.endRow][move.endCol][1] == 'Q'):
                threats.append((move.endRow,move.endCol))
            elif(self.board[move.endRow][move.endCol][1] == 'B' and (king_pos[0]!=move.endRow and king_pos[1]!=move.endCol)):
                threats.append((move.endRow,move.endCol))
            elif(self.board[move.endRow][move.endCol][1] == 'R' and (king_pos[0]==move.endRow or king_pos[1]==move.endCol)):
                threats.append((move.endRow,move.endCol))
        
        self.moves = []
        self.getKnightMoves(king_pos[0],king_pos[1],[])
        for move in self.moves:
            if(self.board[move.endRow][move.endCol][1] == 'N'):
                threats.append((move.endRow,move.endCol))
        
        self.moves = []
        self.getPawnMoves(king_pos[0],king_pos[1],[])
        for move in self.moves:
            if(self.board[move.endRow][move.endCol][1] == 'p'):
                threats.append((move.endRow,move.endCol))
        
        # Find all white pieces that are closest to the king
        # Convert the king to find which pieces of its color are closest to him, by using Queen's movement.
        if (self.board[king_pos[0]][king_pos[1]] == "wK"):
            self.board[king_pos[0]][king_pos[1]] = "bK"
        else:
            self.board[king_pos[0]][king_pos[1]] = "wK"

        self.whiteMove = not self.whiteMove
        self.moves = []
        self.getRookMoves(king_pos[0],king_pos[1],[])
        self.getBishopMoves(king_pos[0],king_pos[1],[])
        pinstmp = []
        for move in self.moves:
            
            if(self.board[move.endRow][move.endCol] != "--"):
                pinstmp.append((move.endRow,move.endCol))

        self.whiteMove = not self.whiteMove
        if (self.board[king_pos[0]][king_pos[1]] == "bK"):
            self.board[king_pos[0]][king_pos[1]] = "wK"
        else:
            self.board[king_pos[0]][king_pos[1]] = "bK"

        
        # Check if each of the pieces closest to the king is threatened and if so, check if it is a possible threat for the king
        # A pin can be created either by Queen Rook or Bishop
        for pin in pinstmp:
            self.moves = []
            self.getRookMoves(pin[0],pin[1],[])
            self.getBishopMoves(pin[0],pin[1],[])
            for move in self.moves:
                    if (move.pieceCaptured[1] == 'Q' and (self.calculateLine(pin[0],pin[1],[(move.endRow,move.endCol)],(king_pos[0],king_pos[1])))):
                        self.pins.append(pin)
                        self.potentialThreats.append((move.endRow,move.endCol))
                    elif (move.pieceCaptured[1] == 'B' and (pin[0]!=move.endRow and pin[1]!=move.endCol) and (self.calculateLine(pin[0],pin[1],[(move.endRow,move.endCol)],(king_pos[0],king_pos[1])))):
                        self.pins.append(pin)
                        self.potentialThreats.append((move.endRow,move.endCol))
                    elif (move.pieceCaptured[1] == 'R' and (pin[0]==move.endRow or pin[1]==move.endCol) and (self.calculateLine(pin[0],pin[1],[(move.endRow,move.endCol)],(king_pos[0],king_pos[1])))):
                        self.pins.append(pin)
                        self.potentialThreats.append((move.endRow,move.endCol))

        return threats

    
    def calculateLine(self,x,y,threats,king):
        '''
        Calculate the line between the piece(x,y) and the king.
        Calculate the line between each threat and the king.
        Return True if these two lines have the same slope(angle) and the piece is closer to the king than the threat.
        If validity is True it means that the piece can move in front of the king to deflect the attack.
        '''
        validity = False
        if (len(threats)==0):
            validity = True
        else: 
            for threat in threats:
                
                if (threat[1]-king[1] == 0 ):
                    slope1 = 10000
                else:
                    slope1 = (threat[0] - king[0]) / (threat[1] - king[1])
                if (y-king[1]== 0): 
                    slope2 = 10000
                else:
                    slope2 = (x - king[0]) / (y - king[1])
                
                euclideanDistance1 = math.sqrt(pow(x-king[0], 2) + pow(y-king[1],2))
                euclideanDistance2 = math.sqrt(pow(threat[0]-king[0], 2) + pow(threat[1]-king[1],2))
                euclideanDistance3 = math.sqrt(pow(threat[0]-king[0], 2) + pow(threat[1]-king[1],2))
                if ( slope1 == slope2 and euclideanDistance1 <= euclideanDistance2 and euclideanDistance2 <= euclideanDistance3):
                    validity = True
         
        return validity

    
    def findPins(self,x,y,pins):
        # Check if a piece is involved in a pin
        for pin in pins:
            if pin[0] == x and pin[1] == y:
                return False
        
        return True

    def checkCastling(self,king_x,king_y,rook_y, canCastle):
        '''
        Takes as input the position of the king, the position of the rook and canCastle list that tracks if the king or the rooks have been moved.
        Return True if there are no pieces between the king and the rook, that means castling is feasible.
        '''
        castling = False
        if (rook_y < king_y and not canCastle[0]):
            castling = True
            for y in range(rook_y+1,king_y):
                if (self.board[king_x][y] != "--"):
                    castling = False
        elif  (rook_y > king_y and not canCastle[1]):
            castling = True
            for y in range(king_y+1,rook_y):
                if (self.board[king_x][y] != "--"):
                    castling = False
        
        return castling
    
  
