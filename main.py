"""
Main will be responsible of displaying the graphics and current chessengine object
"""

import pygame as pg
import ChessGame
import Actions

WIDTH = HEIGHT = 768
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 40
IMAGES = {} 
pg.init()

def loadImages():
    gallery = ['wp','wR','wB','wK','wQ','wN','bp','bR','bB','bK','bQ','bN']
    for pic in gallery:
        IMAGES[pic] = pg.transform.scale(pg.image.load("images/" + pic + ".png"), (SQUARE_SIZE,SQUARE_SIZE))


def drawBoard(display):
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            if ((x+y)%2 == 0 ):
                pg.draw.rect(display,pg.Color("light gray"),pg.Rect(x*SQUARE_SIZE,y*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            else:
                pg.draw.rect(display,pg.Color("gray"),pg.Rect(x*SQUARE_SIZE,y*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))


def drawPieces(display,board):
     for x in range(DIMENSION):
        for y in range(DIMENSION):
            piece = board[x][y]
            if piece != "--":
                display.blit(IMAGES[piece],pg.Rect(y*SQUARE_SIZE,x*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))



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
                    piecePositions.append(square)
                if len(piecePositions) == 2:
                    move  = Actions.Move(piecePositions[0],piecePositions[1],game_state.board)
                    for vm in validMoves:
                        if (move.startRow == vm.startRow and move.startCol == vm.startCol
                            and move.endRow == vm.endRow and move.endCol == vm.endCol):
                                game_state.makeMove(move)
                                moved = True

                    square = ()
                    piecePositions =[]

        if moved:
            validMoves = game_state.getValidMoves()
            if (len(validMoves) == 0):
                print("im here")
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