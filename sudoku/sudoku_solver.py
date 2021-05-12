# Sudoku Solver - solves a given 9x9 solvable sudoku puzzle

import copy



# Returns the solution to the given puzzle
# Returns the original grid if there is no solution
def get_solution(grid):
    if (solve(grid)):
        solve(grid)
        return grid
    else:
        return grid



# Solves a given Sudoku puzzle
def solve(grid):

    empty_spot = find_next_empty(grid)

    # no more empty spots, we've filled the grid with the correct solution
    if (not empty_spot): 
        return True
    else:
        row, col = empty_spot

        for value in range(1, 10):

            # if this is a valid entry, assign the value
            if safe_spot(grid, value, row, col): 
                grid[row][col] = value
                
                # if we can continue with this assignment and find a solution
                if(solve(grid)): 
                    return True
                
                # we cannot solve it with this value, so reset
                grid[row][col] = 0 

        return False



# Finds and returns the next empty spot on the grid
# Returns None if there are no empty spots left
def find_next_empty(grid):
    for i in range(9):
        for j in range(9):
            if (grid[i][j] == 0):
                return (i, j)        
    return None



# Determines if the given value is safe to put at the given spot
def safe_spot(grid, value, row, col):

    # check if the value is already in the column
    for i in range(9):
        if(grid[i][col] == value and row != i):
            return False
    
    # check if the value is already in the row
    for j in range(9):
        if(grid[row][j] == value and col != j):  
            return False
            
    # check if the value is already in the 3x3 grid
    if(is_in_grid(grid, value, row, col)):
        return False

    return True


# Determines if the given value is already in its 3x3 grid 
def is_in_grid(grid, value, row, col):
    top_left_row, top_left_col = get_grid_top_left(row, col)

    for i in range(top_left_row, top_left_row + 3):  
        for j in range(top_left_col, top_left_col + 3):
            if(grid[i][j] == value and (i, j) != (row, col)):
                return True
    return False


# Returns the top left spot of the 3x3 grid that the given spot is in
def get_grid_top_left(row, col):

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




# Prints the grid
def print_grid(grid):
    temp = "-------------------------------------\n"
    for i in range(9):
        if (i == 3 or i == 6):
            temp += "-------------------------------------\n"

        for j in range(9):
            if(j == 0):
                temp += "| " + str(grid[i][j]) + " | "
            elif(j == 8):
                temp += str(grid[i][j]) + " |"
            else:
                temp += str(grid[i][j]) + " | "
        temp += '\n'
    temp += "-------------------------------------" 
    print(temp)




# grid=[[9, 0, 0, 0, 0, 0, 4, 0, 3],
#        [7, 0, 0, 0, 5, 1, 9, 2, 0],
#        [0, 4, 5, 6, 0, 0, 8, 1, 0],
#        [0, 1, 2, 0, 6, 0, 0, 0, 5],
#        [6, 0, 0, 0, 0, 0, 2, 0, 8],
#        [0, 0, 0, 7, 3, 2, 1, 6, 0],
#        [0, 7, 4, 3, 2, 0, 0, 8, 9],
#        [0, 0, 0, 1, 0, 5, 0, 4, 0],
#        [0, 0, 0, 8, 0, 9, 3, 7, 0]]

# print(grid)
# solve(grid)
# print(grid)