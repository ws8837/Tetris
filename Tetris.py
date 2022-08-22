# Tetris
# @Author: Shijie Wang
# @Email: Shijiew21@gmail.com

from tkinter import *
import math
import random
import copy


# init
def init(data):
    data.margin = 20 # margin width for tetris
    data.rows = 40 # total rows for tetris
    data.cols = 20 # total columns for tetris
    data.score = 0  # player's score
    data.mode = "menu" # All modes: menu, pause, play, over, instruction
    data.cellSize = (data.height - data.margin*2)//data.rows # set cell size
    data.emptyColor = "grey" # set emptyColor to blue(color for empty cell)
    data.board = getBoard(data) # set tetris board
    data.tempScore = 0 # temporary score for displaying
    initializePieces(data) # set a list of tetris pieces in data
    data.tetrisPieceColors = ["white"] # set tetris colors for pieces
    newFallingPiece(data) # generate new falling piece

# Reset the game for restart
def reset(data):
    data.score = 0  # player's score
    data.board = getBoard(data) # set tetris board
    data.tetrisPieceColors = ["white"] # set tetris colors for pieces
    newFallingPiece(data) # generate new falling piece

def mousePressed(event, data):
    # use event.x and event.y
    x = event.x
    y = event.y
    if data.mode == "over":
        if data.width//2-55 < x < data.width//4+150 and data.height//4+30 < y < data.height//4+90:
            data.mode = "play"
            reset(data)
        if data.width//2-55 < x < data.width//4+150 and data.height//4+140 < y < data.height//4+200:
            data.mode = "menu"
            reset(data)
    elif data.mode == "menu":
        if data.width//2-85 < x < data.width//4+170 and data.height//4+30 < y < data.height//4+90:
            data.mode = "play"
        if data.width//2-85 < x < data.width//4+170 and data.height//4+140 < y < data.height//4+200:
            data.mode = "instruction"

def keyPressed(event, data):
    # use event.char and event.keysym
    # moving pieces
    if event.keysym == "t":
        print(data.mode)
    if(not data.mode == "over"):
        if event.keysym == "Up": rotateFallingPiece(data)
        elif event.keysym == "Left": moveFallingPiece(data, 0, -1)
        elif event.keysym == "Right": moveFallingPiece(data, 0, 1)
        elif event.keysym == "p": data.mode = "pause"
    if data.mode == "instruction":
        if event.keysym == "r":
            data.mode = "menu"

def timerFired(data):
    if data.mode == "play":
        removeFullRows(data)
        if(not data.mode == "over"):
            moveFallingPiece(data,1,0)

def redrawAll(canvas, data):
    # draw in canvas
    # if the player is at menu
    if data.mode == "menu":
        canvas.create_text(data.width//2+50, 20, text="Highest Score: "+str(readScore()),
        anchor=SW,fill="lightgreen", font="Times 15 bold")
        drawMenu(canvas, data)
    # if the player is playing the game
    elif data.mode == "play":
        drawBoard(canvas, data) # draw board
        drawFallingPiece(canvas, data) # draw falling piece
        canvas.create_text(data.width//2-160, 20, text="Score: "+str(data.score),
        anchor=SW,fill="lightgreen", font="Times 15 bold")
        canvas.create_text(data.width/2+50,20,text="HighestScore:"+str(readScore()),
        anchor=SW,fill="lightgreen", font="Times 15 bold")
        if(data.mode == "over"):
            canvas.create_text(data.width//2-120, data.height//2, text="Game Over",
            anchor=SW, fill="black", font="Times 50 bold")
    # if the player loses
    elif data.mode == "over":
        canvas.create_text(data.width//2-160, 20, text="Score: "+str(data.tempScore),
        anchor=SW,fill="lightgreen", font="Times 15 bold")
        canvas.create_text(data.width//2+50, 20, text="Highest Score:     "+str(readScore()),
        anchor=SW,fill="lightgreen", font="Times 15 bold")
        drawOver(canvas, data)
    # if the mode is instruction page
    elif data.mode == "instruction":
        canvas.create_text(data.width//2-170, 200, text="Press left and right keys to move the pieces. Press \nup key to rotate pieces. Everytime a row is filled up,\n the row will be removed and your score will increase \nby one. The highest score is recorded for everytime \nyou play the game.",anchor=SW,fill="lightgreen", font="Times 15 bold")
        canvas.create_text(data.width//2-85, 400, text="Press R to return to menu",anchor=SW,fill="lightgreen", font="Times 15 bold")

# Draw the game over setting
def drawOver(canvas, data):
    canvas.create_text(data.width//4-30, data.height//4, text="Game Over",
    anchor=SW, fill="lightgreen", font="Times 50 bold")

    # Restart Button
    canvas.create_rectangle(data.width//2-55, data.height//4+30,
    data.width//4+150, data.height//4+90,fill="lightgreen", width=0)

    canvas.create_text(data.width//4+45, data.height//4+75, text="Restart",
    anchor=SW, fill="grey", font="Times 30 bold")

    # Menu Button
    canvas.create_rectangle(data.width//2-55, data.height//4+140,
    data.width//4+150, data.height//4+200,fill="lightgreen", width=0)

    canvas.create_text(data.width//4+45, data.height//4+185, text=" Menu",
    anchor=SW, fill="grey", font="Times 30 bold")

# Draw the menu page
def drawMenu(canvas, data):
    canvas.create_text(data.width//4-30, data.height//4, text="    Tetris",
    anchor=SW, fill="lightgreen", font="Times 50 bold")

    # Play Button
    canvas.create_rectangle(data.width//2-85, data.height//4+30,
    data.width//4+170, data.height//4+90,fill="lightgreen", width=0)

    canvas.create_text(data.width//4, data.height//4+75, text="        Play",
    anchor=SW, fill="grey", font="Times 30 bold")

    # Instruction Button
    canvas.create_rectangle(data.width//2-85, data.height//4+140,
    data.width//4+170, data.height//4+200,fill="lightgreen", width=0)

    canvas.create_text(data.width//4+10, data.height//4+185, text="How to Play",
    anchor=SW, fill="grey", font="Times 30 bold")

# Record highest score
def readScore():
    file = open("Score.txt","r")
    l = file.readlines()
    file.close()
    return int(l[0])

def recordScore(data):
    if readScore() < data.score:
        file = open("Score.txt", "w")
        file.write(str(data.score))
        file.close()

# check for game over
def gameOver(data):
    for i in range(len(data.board[0])):
        if(data.board[0][i] != data.emptyColor):
            data.tempScore = data.score
            return True
    return False













# clear full rows
def removeFullRows(data):
    for i in range(len(data.board)):
        temp = True
        for j in range(len(data.board[0])):
            if(data.board[i][j] == data.emptyColor):
                temp = False
        if temp:
            data.board.pop(i)
            data.board = [[data.emptyColor]*data.cols]+ data.board
            data.score += 1

# draw board
def drawBoard(canvas, data):
    for x in range(data.cols):
        for y in range(data.rows):
            drawCell(canvas, data, y, x)

# draw cells
def drawCell(canvas, data, row, col):
    canvas.create_rectangle(data.margin+data.cellSize*col, data.margin+data.
    cellSize*row,data.margin+data.cellSize*(col+1), data.margin+data.
    cellSize*(row+1), fill=data.board[row][col], width=1)

# generating board
def getBoard(data):
    board = []
    for i in range(data.rows):
        temp = []
        for j in range(data.cols):
            temp.append(data.emptyColor)
        board.append(temp)
    return board

# setting the data.tetrisPieces in init (too long to put it in init)
def initializePieces(data):
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]]
    data.tetrisPieces = [ iPiece, jPiece, lPiece,
    oPiece, sPiece, tPiece, zPiece ] # list of tetris pieces

# creating new falling piece
def newFallingPiece(data):
    data.fallingPiece = data.tetrisPieces[random.randint(0, len(data.
    tetrisPieces) - 1)]
    data.fallingPieceColor = data.tetrisPieceColors[random.randint(0,
    len(data.tetrisPieceColors) - 1)]
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2
    data.fallingPieceCol -= data.fallingPieceCol//2

# move falling piece
def moveFallingPiece(data, drow, dcol):
    data.fallingPieceCol += dcol
    if not fallingPieceIsLegal(data, data.fallingPiece):
        data.fallingPieceCol -= dcol

    data.fallingPieceRow += drow
    placeFallingPiece(data, drow, dcol)

# place the falling piece in board
def placeFallingPiece(data, drow, dcol):
    if not fallingPieceIsLegal(data, data.fallingPiece):
        data.fallingPieceRow -= drow
        for i in range(len(data.fallingPiece)):
            for j in range(len(data.fallingPiece[0])):
                if data.fallingPiece[i][j] == True:
                    data.board[i+data.fallingPieceRow][j+data.fallingPieceCol] = data.fallingPieceColor
        newFallingPiece(data)
        if(gameOver(data)):
            data.mode = "over"
            recordScore(data)

# checking for whether falling piece is on board or on non-empty cell
def fallingPieceIsLegal(data, fallingPiece):
    for y in range(len(fallingPiece)):
        for x in range(len(fallingPiece[0])):
            if(x+data.fallingPieceCol >= data.cols or x+data.fallingPieceCol <0
            or y+data.fallingPieceRow >= data.rows or x+data.fallingPieceRow
            <0): return False
            if(data.board[y+data.fallingPieceRow][x+data.fallingPieceCol] !=
            data.emptyColor and fallingPiece[y][x] == True):
                    return False
    return True

# draw the falling piece
def drawFallingPiece(canvas, data):
    color = data.fallingPieceColor
    piece = data.fallingPiece
    if(not data.mode == "over"):
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if(piece[y][x] == True):
                    canvas.create_rectangle(data.margin+data.cellSize*(x+data.
                    fallingPieceCol),data.margin+data.cellSize*(y+data.
                    fallingPieceRow),data.margin+data.cellSize*(x+data.
                    fallingPieceCol+1),data.margin+data.cellSize*(y+data.
                    fallingPieceRow+1), fill=color, width=1)

# rotate falling piece
def rotateFallingPiece(data):
    oldRow = data.fallingPieceRow
    oldCol = data.fallingPieceCol
    oldPiece = copy.deepcopy(data.fallingPiece)
    centerRow = data.fallingPieceRow + len(data.fallingPiece)//2
    centerCol = data.fallingPieceCol + len(data.fallingPiece[0])//2
    newRow = centerRow - len(data.fallingPiece[0])//2
    newCol = centerCol - len(data.fallingPiece)//2
    data.fallingPieceCol = newCol
    data.fallingPieceRow = newRow
    data.fallingPiece = newDimension(data)
    if not fallingPieceIsLegal(data, data.fallingPiece):
        data.fallingPieceCol = oldCol
        data.fallingPieceRow = oldRow
        data.fallingPiece = oldPiece

# changing the dimension of the falling piece and rotate it
def newDimension(data):
    newPiece = []
    for i in range(len(data.fallingPiece[0])):
        temp = []
        for j in range(len(data.fallingPiece)):
            temp.append(data.fallingPiece[j][len(data.fallingPiece[0])-1-i])
        newPiece.append(temp)
    return newPiece


def run(width=360, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.grid(row=0, column=0)
    
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))

    timerFiredWrapper(canvas, data)
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

# Run the program
def playTetris(rows=15, cols=10):
    # use the rows and cols to compute the appropriate window size here!
    run()

# run tetris
playTetris()
