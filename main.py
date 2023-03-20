"""
Main will be responsible of displaying the graphics and current chessengine object
"""

import pygame as pg
import ChessGame
import Actions
import minmax

WIDTH = HEIGHT = 864
DIMENSION = 9
SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 40
IMAGES = {} 
pg.init()
font = pg.font.SysFont('Arial', 25)

'''
Load all images for the pieces
'''
def loadImages():
    gallery = ['wp','wR','wB','wK','wQ','wN','bp','bR','bB','bK','bQ','bN']
    for pic in gallery:
        IMAGES[pic] = pg.transform.scale(pg.image.load("images/" + pic + ".png"), (SQUARE_SIZE,SQUARE_SIZE))


'''
Draw the grid (8x8) and leave one dimension for the pawn promotion graphics 
'''
def drawBoard(display):
    for x in range(DIMENSION-1):
        for y in range(DIMENSION-1):
            if ((x+y)%2 == 0 ):
                pg.draw.rect(display,pg.Color("light gray"),pg.Rect(x*SQUARE_SIZE,y*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            else:
                pg.draw.rect(display,pg.Color("gray"),pg.Rect(x*SQUARE_SIZE,y*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))

'''
Complete drawing the board by putting each piece on the grid based on the board of ChessGame object
'''
def drawPieces(display,board):
     for x in range(DIMENSION-1):
        for y in range(DIMENSION-1):
            piece = board[x][y]
            if piece != "--":
                display.blit(IMAGES[piece],pg.Rect(y*SQUARE_SIZE,x*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))

'''
Draw the pieces that can replace the pawn when it reaches last rank (pawn promotion)
'''
def drawPromotionPieces(display,color):
    pg.draw.rect(display,pg.Color("light gray"),pg.Rect(8*SQUARE_SIZE,2*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    pg.draw.rect(display,pg.Color("light gray"),pg.Rect(8*SQUARE_SIZE,3*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    pg.draw.rect(display,pg.Color("light gray"),pg.Rect(8*SQUARE_SIZE,4*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    pg.draw.rect(display,pg.Color("light gray"),pg.Rect(8*SQUARE_SIZE,5*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    display.blit(IMAGES[color + "Q"],pg.Rect(8*SQUARE_SIZE,2*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    display.blit(IMAGES[color + "R"],pg.Rect(8*SQUARE_SIZE,3*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    display.blit(IMAGES[color + "B"],pg.Rect(8*SQUARE_SIZE,4*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
    display.blit(IMAGES[color + "N"],pg.Rect(8*SQUARE_SIZE,5*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))

'''
Function that tracks the selection of the piece that will replace the promotion pawn
'''
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

'''
Highlight the valid moves for each piece on the board
'''
def highlightMoves(display, validMoves , square_selected , game_state):
    if square_selected != () :
        x = square_selected[0]
        y = square_selected[1]
        # If is white's turn to move focus on white pieces else on black
        try:
            if game_state.board[x][y][0] == ('w' if game_state.whiteMove else 'b'):
                if(x==8):
                    print(x)
                    print(y)
                    print(game_state.board[x][y][0])
                # Create the instance that will highlight the squares
                square_highlighted = pg.Surface((SQUARE_SIZE,SQUARE_SIZE))
                square_highlighted.set_alpha(30)
                square_highlighted.fill(pg.Color('green'))
                display.blit(square_highlighted, (y*SQUARE_SIZE, x*SQUARE_SIZE))
                square_highlighted.set_alpha(100)
                square_highlighted.fill(pg.Color('yellow'))
                for move in validMoves:
                    if (move.startRow == x and move.startCol == y):
                        display.blit(square_highlighted, (move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE))
        

        except:
            print("INDEX ERROR")
            print(square_selected)

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
    moved = False #Track if player has made a move
    promotion = False #Track if pawn is on last rank and player has to choose a piece
    checkmate = False #Track checkmate
    stalemate = False #Track stalemate
    winner = ""
    isMachineWhite = False #False for blacks
    while playingMode:
        if game_state.whiteMove != isMachineWhite:
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
                        # If player has not yet chose piece on promotion do not continue the game
                        if not promotion:
                            piecePositions.append(square)
                    if len(piecePositions) == 2:
                        try:
                            move  = Actions.Move(piecePositions[0],piecePositions[1],game_state.board)
                        except:
                            print("CLICKED OUT OF THE BOARD EXCEPTION")
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
                elif event.type == pg.KEYDOWN:
                    #When enter is pressed reset the game state
                    if event.key == pg.K_RETURN:
                        del game_state
                        display.fill(pg.Color("white"))
                        game_state = ChessGame.GameState()
                        square = () # tuple that stores the current selected square
                        piecePositions = [] # starting position and destination
                        validMoves = game_state.getValidMoves()
                        moved = False
                        promotion = False
                        checkmate = False
                        stalemate = False
                        winner = ""
        else: 
            # If player has not yet chose piece on promotion do not continue the game
            if not promotion:
                    piecePositions.append(square)
            if len(piecePositions) == 2:
                move = minmax.getNextMove(game_state.board, isMachineWhite)
                if (move != "NOT YET CALCULATED"):
                    game_state.makeMove(move)
                    if (game_state.blackPawnsPromo or game_state.whitePawnsPromo):
                        moved = False
                        promotion = True
                    else: 
                        moved = True
                    tmpMovedX = move.endRow
                    tmpMovedY = move.endCol
                else: 
                    game_state.whiteMove = not game_state.whiteMove
            
                square = ()
                piecePositions =[]
            if (game_state.blackPawnsPromo and not moved):
                display.blit(IMAGES["bQ"],pg.Rect(move.endRow*SQUARE_SIZE,move.endCol*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
                game_state.board[move.endRow][move.endCol] = "bQ"
                moved = True
                promotion = not moved

            elif (game_state.whitePawnsPromo and not moved):
                display.blit(IMAGES["wQ"],pg.Rect(move.endRow*SQUARE_SIZE,move.endCol*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
                game_state.board[move.endRow][move.endCol] = "wQ"
                moved = True
                promotion = not moved                   
        

        if moved:
            validMoves = game_state.getValidMoves()
            display.fill(pg.Color("white"))
            if (len(validMoves) == 0):
                if (len(game_state.threats) == 0):
                    stalemate = True
                else:
                    if (not game_state.whiteMove):
                        winner = "White"
                    else:
                        winner = "Black"
                    checkmate = True
            moved = False

        drawBoard(display)
        highlightMoves(display,validMoves,square,game_state)
        drawPieces(display, game_state.board) # piece highlighting or move suggestions can be added later on here
        if checkmate: 
            display.fill(pg.Color("white"))
            pg.draw.rect(display, (210, 210, 210), (302,302, 330,60), 6)
            display.blit(font.render('Checkmate! ' + winner + " wins the game!", True, (0,0,0)), (310,320))
            pg.draw.rect(display, (210, 210, 210), (312,402, 310,60), 2)
            display.blit(font.render("Press ENTER to play again!", True, (0,0,0)), (320,420))
        elif stalemate:
            display.fill(pg.Color("white"))
            pg.draw.rect(display, (210, 210, 210), (396,402, 120,100), 5)
            display.blit(font.render('Stalemate! It is a Draw!', True, (0,0,0)), (350,420))
            pg.draw.rect(display, (210, 210, 210), (396,502, 120,100), 5)
            display.blit(font.render("Press ENTER to play again!", True, (0,0,0)), (350,420))


        clock.tick(MAX_FPS)
        pg.display.flip()



if __name__ == "__main__":  
    main()