# Sudoku Generator - generates a random 9x9 solvable sudoku puzzle

import random
import copy
import math
import sudoku_solver


class SudokuGenerator():
    def __init__(self, num_min_clues):
        self.num_min_clues = num_min_clues
        self.counter = 0
        self.path = []
        self.grid = [[0 for i in range(9)] for j in range(9)]
   
        self.original = copy.deepcopy(self.grid)
        self.generate_puzzle()
    


    # Returns the generated puzzle
    def get_puzzle(self):
        return self.grid
        
        

    # Generates a Sudoku Puzzle
    def generate_puzzle(self):
        self.generate_solution(self.grid)
        self.remove_nums_from_grid()
        return
    


    # Generates a full, complete solution with backtracking
    def generate_solution(self, grid):

        num_list = [1,2,3,4,5,6,7,8,9]

        for i in range(81):
            row = i // 9
            col = i % 9

            # find next empty cell
            if (grid[row][col] == 0):
                random.shuffle(num_list)

                for num in num_list:
                    if sudoku_solver.safe_spot(grid, num, row, col):
                        self.path.append((num, row, col))
                        grid[row][col] = num

                        if not sudoku_solver.find_next_empty(grid):
                            return True
                        else:
                            # if the grid is full
                            if self.generate_solution(grid):
                                return True
                break
        grid[row][col] = 0
        return False
    


    # Returns a shuffled list of all non-empty values in the grid
    def get_non_empty_squares(self, grid):
        squares = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0:
                    squares.append((i, j))
        random.shuffle(squares)
        return squares
    


    # Remove numbers from the grid to create the starting puzzle
    def remove_nums_from_grid(self):

        # get all non-empty squares from the grid
        non_empty_squares = self.get_non_empty_squares(self.grid)
        non_empty_squares_count = len(non_empty_squares)

        # decremented for each non-unique solution found
        rounds = 3

        # minimum 17 clues
        while rounds > 0 and non_empty_squares_count >= self.num_min_clues:
            row, col = non_empty_squares.pop()
            non_empty_squares_count -= 1

            removed_square = self.grid[row][col]
            self.grid[row][col] = 0

            grid_copy = copy.deepcopy(self.grid)

            self.counter = 0

            if(sudoku_solver.solve(grid_copy)):
                sudoku_solver.solve(grid_copy)
                self.counter += 1
            
            if self.counter != 1:
                self.grid[row][col] = removed_square
                non_empty_squares_count += 1
                rounds -= 1
        return
    


    # Print the generated puzzle
    def print_puzzle(self):
        sudoku_solver.print_grid(self.grid)

