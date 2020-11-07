from tkinter import *
root = Tk()







# Sudoku Solver

#solves a given Sudoku board
def solve(board):

    """
    board  --- given Sudoku board with some amount of fixed spots
    row    --- current row
    """

    emptySpot = findNextEmpty(board)

    if(emptySpot == None): #no more empty spots, we've filled the board with the correct solution
        return True
    else:
        row, col = emptySpot

        for value in range(1,10):
            if safeSpot(board, value, row, col): #if this is a valid entry, assign the value
                board[row][col] = value
                
                if(solve(board)): #if we can continue with this assignment and find a solution
                    return True
                
                board[row][col] = 0 #we cannot solve it with this value, so reset

        return False
 
                

        
#finds and returns the next empty spot on the board as a tuple (going across, then down)
#returns None if no empty spots left
def findNextEmpty(board):
    for i in range(9):
        for j in range(9):
            if(board[i][j] == 0):
                return (i, j)
            
    return None


#determines if the given value (1-9) is safe
#to put at the given board spot (row and col)
def safeSpot(board, value, row, col):

    if(board[row][col] != 0): #if the spot is filled, return False
        return False

    for i in range(0,8):
        if(board[i][col] == value and i != row):  #if the column already has that value in it
            return False
        
    for j in range(0,8):
        if(board[row][j] == value and j != col):  #if the row already has that value in it
            return False
            
    if(isInGrid(board, value, row, col)): #if the value is already in the 3x3 grid
        return False

    return True


#determines if the given value is already in its 3x3 grid 
def isInGrid(board, value, row, col):
    gridRow, gridCol = getGridTopLeft(row, col)

    for i in range(gridRow, gridRow + 3):      #3x3 grid rows
        for j in range(gridCol, gridCol + 3):  #3x3 grid cols
            if(board[i][j] == value and i!=row and j!=col):
                return True
    return False


#returns the top left spot of the 3x3 grid that
#the given row and col spot is in
def getGridTopLeft(row, col):
    
    if(row==0 or row==1 or row==2):
        if(col==0 or col==1 or col==2):
            return (0, 0)                       #grid 1 top left
        elif(col==3 or col==4 or col==5):
            return (0, 3)                       #grid 2 top left
        else:
            return (0, 6)                       #grid 3 top left
    elif(row==3 or row==4 or row==5):
        if(col==0 or col==1 or col==2):
            return (3, 0)                       #grid 4 top left
        elif(col==3 or col==4 or col==5):
            return (3, 3)                       #grid 5 top left
        else:
            return (3, 6)                       #grid 6 top left
    else:
       if(col==0 or col==1 or col==2):
           return (6, 0)                        #grid 7 top left
       elif(col==3 or col==4 or col==5):
           return (6, 3)                        #grid 8 top left
       else:
           return (6, 6)                        #grid 9 top left













root.title("Sudoku")


'''
WISH LIST:


-enter a number
    -correct? keep it
    -incorrect? delete it

-lives/lives lost

-if len(labelsList = 81) --> SOLVED!
    
'''

board=[[9, 0, 0, 0, 0, 0, 4, 0, 3],
            [7, 0, 0, 0, 5, 1, 9, 2, 0],
            [0, 4, 5, 6, 0, 0, 8, 1, 0],
            [0, 1, 2, 0, 6, 0, 0, 0, 5],
            [6, 0, 0, 0, 0, 0, 2, 0, 8],
            [0, 0, 0, 7, 3, 2, 1, 6, 0],
            [0, 7, 4, 3, 2, 0, 0, 8, 9],
            [0, 0, 0, 1, 0, 5, 0, 4, 0],
            [0, 0, 0, 8, 0, 9, 3, 7, 0]]

boardCopy = [[9, 0, 0, 0, 0, 0, 4, 0, 3],
            [7, 0, 0, 0, 5, 1, 9, 2, 0],
            [0, 4, 5, 6, 0, 0, 8, 1, 0],
            [0, 1, 2, 0, 6, 0, 0, 0, 5],
            [6, 0, 0, 0, 0, 0, 2, 0, 8],
            [0, 0, 0, 7, 3, 2, 1, 6, 0],
            [0, 7, 4, 3, 2, 0, 0, 8, 9],
            [0, 0, 0, 1, 0, 5, 0, 4, 0],
            [0, 0, 0, 8, 0, 9, 3, 7, 0]]
solution = solve(boardCopy)



labelsList = [] # list of fixed labels
lives = 3


# Makes the entries
for i in range(9):
    for j in range(9):

        # If the current space on the starter board is already filled
        if(board[i][j] != 0):    
            temp = Label(root, text=str(board[i][j]), width=2, borderwidth=.50, relief='solid') # creates the Label
            labelsList.append(temp)     # adds it to the list of labels
            temp.grid(row=i, column=j)   # puts the new label on the grid
        else:
            temp = Entry(root, text="", width=2, borderwidth=0.5, justify='center', relief='solid')
            temp.grid(row=i, column=j)




# user entered a guess, takes the entry, and the row and column of the entry
def myEntry(entry, i, j):
    if(entry == solution[i][j]):
        board[i][j] = entry
        labelsList.append(temp)
    else:
        lives - 1



root.mainloop()


















    
        
            

















    

