"""
Main will be responsible of displaying the graphics and current chessengine object
"""

import pygame as pg
import ChessGame

WIDTH = HEIGHT = 768
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 40
IMAGES = {} 
pg.init()

def loadImages():
    IMAGES['wp'] = pg.transform.scale(pg.image.load("images/wp.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['wR'] = pg.transform.scale(pg.image.load("images/wR.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['wB'] = pg.transform.scale(pg.image.load("images/wB.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['wK'] = pg.transform.scale(pg.image.load("images/wK.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['wQ'] = pg.transform.scale(pg.image.load("images/wQ.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['wN'] = pg.transform.scale(pg.image.load("images/wN.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['bp'] = pg.transform.scale(pg.image.load("images/bp.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['bR'] = pg.transform.scale(pg.image.load("images/bR.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['bB'] = pg.transform.scale(pg.image.load("images/bB.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['bK'] = pg.transform.scale(pg.image.load("images/bK.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['bQ'] = pg.transform.scale(pg.image.load("images/bQ.png"), (SQUARE_SIZE,SQUARE_SIZE))
    IMAGES['bN'] = pg.transform.scale(pg.image.load("images/bN.png"), (SQUARE_SIZE,SQUARE_SIZE))


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
            if piece != " ":
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
    while playingMode:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playingMode = False
        clock.tick(MAX_FPS)
        pg.display.flip()



if __name__ == "__main__":  
    main()