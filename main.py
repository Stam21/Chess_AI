"""
Main will be responsible of displaying the graphics and current chessengine object
"""

import pygame as pg
import ChessGame
import Actions

WIDTH = HEIGHT = 864
DIMENSION = 9
SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 40
IMAGES = {} 
pg.init()

def loadImages():
    gallery = ['wp','wR','wB','wK','wQ','wN','bp','bR','bB','bK','bQ','bN']
    for pic in gallery:
        IMAGES[pic] = pg.transform.scale(pg.image.load("images/" + pic + ".png"), (SQUARE_SIZE,SQUARE_SIZE))


def drawBoard(display):
    for x in range(DIMENSION-1):
        for y in range(DIMENSION-1):
            if ((x+y)%2 == 0 ):
                pg.draw.rect(display,pg.Color("light gray"),pg.Rect(x*SQUARE_SIZE,y*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            else:
                pg.draw.rect(display,pg.Color("gray"),pg.Rect(x*SQUARE_SIZE,y*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))


def drawPieces(display,board):
     for x in range(DIMENSION-1):
        for y in range(DIMENSION-1):
            piece = board[x][y]
            if piece != "--":
                display.blit(IMAGES[piece],pg.Rect(y*SQUARE_SIZE,x*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))

def drawPromotionPieces(display,color):
    pg.draw.rect(display,pg.Color("light gray"),pg.Rect(8*SQUARE_SIZE,2*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    pg.draw.rect(display,pg.Color("light gray"),pg.Rect(8*SQUARE_SIZE,3*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    pg.draw.rect(display,pg.Color("light gray"),pg.Rect(8*SQUARE_SIZE,4*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    pg.draw.rect(display,pg.Color("light gray"),pg.Rect(8*SQUARE_SIZE,5*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    display.blit(IMAGES[color + "Q"],pg.Rect(8*SQUARE_SIZE,2*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    display.blit(IMAGES[color + "R"],pg.Rect(8*SQUARE_SIZE,3*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    display.blit(IMAGES[color + "B"],pg.Rect(8*SQUARE_SIZE,4*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    display.blit(IMAGES[color + "N"],pg.Rect(8*SQUARE_SIZE,5*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))

def selectPiece(display,mouse_x,mouse_y,pawn_pos,color,board):

    picked = False
    if (mouse_x == 2 and mouse_y == 8):
        display.blit(IMAGES[color + "Q"],pg.Rect(pawn_pos[1]*SQUARE_SIZE,pawn_pos[0]*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
        board[pawn_pos[0]][pawn_pos[1]] = color + "Q"
        picked = True
    elif (mouse_x == 3 and mouse_y == 8):
        display.blit(IMAGES[color + "R"],pg.Rect(pawn_pos[1]*SQUARE_SIZE,pawn_pos[0]*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
        board[pawn_pos[0]][pawn_pos[1]] = color + "R"
        picked = True
    elif (mouse_x == 4 and mouse_y == 8):
        display.blit(IMAGES[color + "B"],pg.Rect(pawn_pos[1]*SQUARE_SIZE,pawn_pos[0]*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
        board[pawn_pos[0]][pawn_pos[1]] = color + "B"
        picked = True
    elif (mouse_x == 5 and mouse_y == 8): 
        display.blit(IMAGES[color + "N"],pg.Rect(pawn_pos[1]*SQUARE_SIZE,pawn_pos[0]*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
        board[pawn_pos[0]][pawn_pos[1]] = color + "N"
        picked = True
    
    return picked

def main():
    playingMode = True
    display = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    display.fill(pg.Color("white"))
    game_state = ChessGame.GameState()
    loadImages()
    drawBoard(display)
    drawPieces(display,game_state.board)
    square = () # tuple that stores the current selected square
    piecePositions = [] # starting position and destination
    validMoves = game_state.getValidMoves()
    moved = False
    promotion = False
    while playingMode:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playingMode = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_position = pg.mouse.get_pos()
                mouse_x = mouse_position[0]//SQUARE_SIZE
                mouse_y = mouse_position[1]//SQUARE_SIZE
                # check if same square is selected twice
                if (square == (mouse_y,mouse_x)):
                    square = ()
                    piecePositions =[]
                else:
                    square = (mouse_y,mouse_x)
                    if not promotion:
                        piecePositions.append(square)
                if len(piecePositions) == 2:
                    move  = Actions.Move(piecePositions[0],piecePositions[1],game_state.board)
                    for vm in validMoves:
                        if (move.startRow == vm.startRow and move.startCol == vm.startCol
                            and move.endRow == vm.endRow and move.endCol == vm.endCol):
                                game_state.makeMove(move)
                                if (game_state.blackPawnsPromo or game_state.whitePawnsPromo):
                                    moved = False
                                    promotion = True
                                else: 
                                    moved = True
                                tmpMovedX = move.endRow
                                tmpMovedY = move.endCol
                
                    square = ()
                    piecePositions =[]
                if (game_state.blackPawnsPromo and not moved):
                    drawPromotionPieces(display,"b")
                    moved =selectPiece(display,mouse_y,mouse_x,(tmpMovedX,tmpMovedY),"b",game_state.board)
                    promotion = not moved

                elif (game_state.whitePawnsPromo and not moved):
                    drawPromotionPieces(display,"w")
                    moved = selectPiece(display,mouse_y,mouse_x, (tmpMovedX,tmpMovedY),"w",game_state.board)
                    promotion = not moved
            

        

        if moved:
            validMoves = game_state.getValidMoves()
            display.fill(pg.Color("white"))
            if (len(validMoves) == 0):
                if (len(game_state.threats) == 0):
                    print("Stalemate")
                else:
                    print("Checkmate")
            moved = False
        
        drawBoard(display)
        drawPieces(display, game_state.board) # piece highlighting or move suggestions can be added later on here
        clock.tick(MAX_FPS)
        pg.display.flip()



if __name__ == "__main__":  
    main()