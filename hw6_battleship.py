"""
15-110 Hw6 - Battleship Project
Name:
AndrewID:
"""

import hw6_battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
#5 [Check6-1] & #3 [Check6-2] & #3 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data['rows'] = 10
    data['cols'] = 10
    data['boardsize'] = 500
    data['numShips'] = 5
    data['computerBoard'] = emptyGrid(data['rows'], data['cols'])
    data['userBoard'] = emptyGrid(data['rows'], data['cols'])
    data['computerBoard'] = addShips(data['computerBoard'], data['numShips'])
    data['tempShip'] = []
    data['addedShips'] = 0
    data['winner'] = None
    data['maxTurns'] = 50
    data['currTurns'] = 0
    return


'''
makeView(data, userCanvas, compCanvas)
#6 [Check6-1] & #2 [Check6-2] & #3 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data['userBoard'], True)
    drawGrid(data, compCanvas, data['computerBoard'], False)
    drawShip(data, userCanvas, data['tempShip'])
    drawGameOver(data, userCanvas)
    return


'''
keyPressed(data, events)
#5 [Hw6]
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == 'Return':
        makeModel(data)
    pass


'''
mousePressed(data, event, board)
#5 [Check6-2] & #1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; mouse event object ; str
Returns: None
'''
def mousePressed(data, event, board):
    col, row = getClickedCell(data, event)
    col = int(col)
    row = int(row)
    if board == 'user':
        clickUserBoard(data, row, col)
    else:
        if data['addedShips'] == 5:
            runGameTurn(data, row, col)
    return None

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
#1 [Check6-1]
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(1)
        grid.append(row)
    return grid


'''
createShip()
#2 [Check6-1]
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    centerX = random.randint(1,8)
    centerY = random.randint(1,8)
    orientation = random.randint(0,1)
    if orientation == 0:
        ship = [[centerX, centerY - 1], [centerX, centerY], [centerX, centerY + 1]]
    else:
        ship = [[centerX - 1, centerY], [centerX, centerY], [centerX + 1, centerY]]
    return ship


'''
checkShip(grid, ship)
#3 [Check6-1]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for point in ship:
        x, y = point
        x = int(x)
        y = int(y)
        if grid[x][y] != 1:
            return False
    return True


'''
addShips(grid, numShips)
#4 [Check6-1]
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count = 0
    while count < numShips:
        ship = createShip()
        if checkShip(grid, ship):
            for point in ship:
                x, y = point
                grid[x][y] = 2
            count += 1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
#6 [Check6-1] & #1 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    cellWidth = data['boardsize']/data['rows']
    cellHeight = data['boardsize']/data['cols']

    for i in range(data['rows']):
        for j in range(data['cols']):
            if grid[i][j] == 1:
                color = 'blue'
            elif grid[i][j] == 2 and not showShips:
                color = 'blue'
            elif grid[i][j] == 4:
                color = 'red'
            elif grid[i][j] == 3:
                color = 'white'
            elif grid[i][j] == 2:
                color = 'yellow'
            canvas.create_rectangle(i * cellWidth, j * cellHeight, 
                                    (i + 1) * cellWidth, (j + 1) * cellHeight, 
                                    fill = color)
    return



### WEEK 2 ###

'''
isVertical(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship = sorted(ship)
    shipX = ship[0][0]
    shipY = ship[0][1]
    for point in ship[1:]:
        x, y = point
        if y != shipY:
            return False
        if x != shipX + 1:
            return False
        shipX = x
    return True


'''
isHorizontal(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship = sorted(ship)
    shipX = ship[0][0]
    shipY = ship[0][1]
    for point in ship[1:]:
        x, y = point
        if x != shipX:
            return False
        if y != shipY + 1:
            return False
        shipY = y
    return True


'''
getClickedCell(data, event)
#2 [Check6-2]
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    rowWidth = data['boardsize']/data['rows']
    colWidth = data['boardsize']/data['cols']
    row = event.y//rowWidth
    col = event.x//colWidth
    return [row, col]


'''
drawShip(data, canvas, ship)
#3 [Check6-2]
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    cellWidth = data['boardsize']/data['rows']
    cellHeight = data['boardsize']/data['cols']
    for point in ship:
        x, y = point
        canvas.create_rectangle(x * cellWidth, y * cellHeight, 
                                    (x + 1) * cellWidth, (y + 1) * cellHeight, 
                                    fill = 'white')
    return


'''
shipIsValid(grid, ship)
#4 [Check6-2]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid, ship):
        if isHorizontal(ship) or isVertical(ship):
            return True
    return False


'''
placeShip(data)
#4 [Check6-2]
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    userBoard = data['userBoard']
    tempShip = data['tempShip']
    if shipIsValid(userBoard, tempShip):
        for x, y in tempShip:
            x = int(x)
            y = int(y)
            userBoard[x][y] = 2
        data['addedShips'] += 1
    else:
        print('Ship is not valid: Please try again')
    data['tempShip'] = []
    data['userBoard'] = userBoard
    return


'''
clickUserBoard(data, row, col)
#4 [Check6-2]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data['addedShips'] == 5:
        return
    tempShip = data['tempShip']
    if [row, col] in tempShip:
        return
    else:
        tempShip.append([row, col])
        data['tempShip'] = tempShip
    if len(data['tempShip']) == 3:
        placeShip(data)
    if data['addedShips'] == 5:
        print("You may now start the game")
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
#1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == 2:
        board[row][col] = 4
    elif board[row][col] == 1:
        board[row][col] = 3
    if isGameOver(board):
        data['winner'] = player
    return


'''
runGameTurn(data, row, col)
#1 [Hw6] & #2 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    userBoard = data['userBoard']
    compBoard = data['computerBoard']
    if data['winner'] != None:
        return
    if compBoard[row][col] in [3, 4]:
        return
    updateBoard(data, compBoard, row, col, "user")
    guessRow, guessCol = getComputerGuess(userBoard)
    updateBoard(data,userBoard, guessRow, guessCol, "comp")
    data['currTurns'] += 1
    if data['currTurns'] == data['maxTurns']:
        data['winner'] = 'draw'
    return


'''
getComputerGuess(board)
#2 [Hw6]
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    row = random.randint(0, 9)
    col = random.randint(0, 9)
    while board[row][col] in [3, 4]:
        row = random.randint(0, 9)
        col = random.randint(0, 9)
    return [row, col]


'''
isGameOver(board)
#3 [Hw6]
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 2:
                return False
    return True


'''
drawGameOver(data, canvas)
#3 [Hw6] & #4 [Hw6] & #5 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data['winner'] == None:
        return
    canvas.create_rectangle(100, 200, 400, 400, fill = "white")
    canvas.create_text(250, 350, text= "Press Enter to Play Again")
    if data['winner'] == "user":
        canvas.create_text(250, 250, text= "You Win!")
    elif data['winner'] == "draw":
        canvas.create_text(250, 250, text= "Out of Moves: You Drew!")
    elif data['winner'] == "comp":
        canvas.create_text(250, 250, text= "You Lose!")
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()

    ## Uncomment these for Week 2 ##
    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()

    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 TESTS " +  "#" * 16 + "\n")
    test.week3Tests()

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
