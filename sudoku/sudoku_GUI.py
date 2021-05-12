# Sudoku GUI - a Sudoku GUI that combines sudoku_generator.py, 
#              sudoku_solver.py, and the Python Tkinter library for
#              an interactive Sudoku game guaranteed to be solvable.
#
#               MODES:
#                   -Easy   (37-40 clues to start)
#                   -Medium (27-36 clues to start)
#                   -Hard   (19-26 clues to start)
#                   -Expert (17-18 clues to start)


from tkinter import *
from time import time
import copy
import sys
import sudoku_solver 
import sudoku_generator




def start():
    global root
    root = Tk()
    root.title("Sudoku")

    class SudokuGame:

        def __init__(self, root, lives):
            self.root = root
            self.lives = lives
            self.mode = ""



            # INITIALIZE THE ROOT

            self.root.geometry("900x700")
            self.root.configure(bg="lightblue")

            self.root.attributes("-fullscreen", True)
            self.root.bind("<Escape>", self.end_full_screen)


            
            # INITIALIZE THE WELCOME PAGE 


            self.padding_frame = Frame(self.root, bg="lightblue", height=250)
            self.padding_frame.pack()

            self.header_frame = Frame(self.root, bg="lightblue")
            self.header_frame.pack()

            self.button_frame = Frame(self.root, bg="lightblue")
            self.button_frame.pack()

            self.bottom_frame = Frame(self.root, bg="lightblue")
            self.bottom_frame.pack()

            self.header = Label(self.header_frame, text="WELCOME TO SUDOKU!", font="Courier 75 bold", bg="lightblue")
            self.header.pack()
            self.sub_header = Label(self.header_frame, text="Please choose a difficulty level", height=3, bg="lightblue")
            self.sub_header.config(font=("", 45))
            self.sub_header.pack()



            # INITIALIZE THE DIFFICULTY LEVEL BUTTONS

            # padding in between the buttons
            self.button_padding_1 = Label(self.button_frame, text="                   ", bg="lightblue")
            self.button_padding_1.grid(row=0, column=1)
            self.button_padding_2 = Label(self.button_frame, text="                   ", bg="lightblue")
            self.button_padding_2.grid(row=0, column=3)
            self.button_padding_3 = Label(self.button_frame, text="                   ", bg="lightblue")
            self.button_padding_3.grid(row=0, column=5)


            self.mode_selected = IntVar()

            self.easy_button = Button(self.button_frame, text="Easy", height=3, width=10, font="default 20 bold", command=lambda *_, mode="easy", quit=False: self.set_mode(mode, quit))
            self.easy_button.grid(row=0, column=0)

            self.medium_button = Button(self.button_frame, text="Medium", height=3, width=10, font="default 20 bold", command=lambda *_, mode="medium", quit=False: self.set_mode(mode, quit))
            self.medium_button.grid(row=0, column=2)

            self.hard_button = Button(self.button_frame, text="Hard", height=3, width=10, font="default 20 bold", command=lambda *_, mode="hard", quit=False: self.set_mode(mode, quit))
            self.hard_button.grid(row=0, column=4)

            self.expert_button = Button(self.button_frame, text="Expert", height=3, width=10, font="default 20 bold", command=lambda *_, mode="expert", quit=False: self.set_mode(mode, quit))
            self.expert_button.grid(row=0, column=6)


            # EXTRA INFO

            self.bottom_padding = Label(self.bottom_frame, text="", bg="lightblue", height=3)
            self.bottom_padding.pack()

            self.quit_button = Button(self.bottom_frame, text="Quit", height=2, width=8, font="default 14 bold", command=lambda *_, mode="", quit=True: self.set_mode(mode, quit))
            self.quit_button.pack()

            self.escape_message = Label(self.bottom_frame, text="**Press the Escape key to exit full screen mode**", height=5, bg="lightblue")
            self.escape_message.pack()



            # WAIT FOR THE USER TO SELECT A DIFFICULTY MODE

            self.root.wait_variable(self.mode_selected)



             # DESTROY THE WELCOME PAGE
            self.padding_frame.destroy()
            self.header_frame.destroy()
            self.button_frame.destroy()
            self.bottom_frame.destroy()





            # CREATE THE GAME BOARD PAGE
            
            self.initialize_canvas()
            self.generate_board()


            # number of current solved cells
            self.solved = 0

            # list of values left to use on the grid for each number 1 - 9
            self.nums_left_to_use = [9, 9, 9, 9, 9, 9, 9, 9, 9]

            # list of Entry widgets for the unsolved cells
            self.entries = []

            # list of each Entry widget's corresponding StringVar() variable
            self.string_vars = []
          
            self.draw_canvas()

            print(self.nums_left_to_use)
            print(self.solved)




        # Sets the 'mode' variable when the user selects a difficulty
        # If the user presses the quit button on the welcome page, quits the game
        def set_mode(self, mode, quitPressed):
            self.mode_selected.set(1)
            self.mode = mode
            if (quitPressed):
                sys.exit()
        


        # Initialize the canvas
        def initialize_canvas(self):
            self.initialize_frames()
            self.initialize_labels()
            self.initialize_buttons()
       
            # initialize Escape Key information
            self.escape_message = Label(self.escape_message_frame, text="**Press the Escape key to exit full screen mode**", height=5, bg="lightblue")
            self.escape_message.pack()

        

        # Initialize all of the Frame widgets
        def initialize_frames(self):
            #frame to pad the rest of the frames
            self.padding_frame = Frame(self.root, bg="lightblue", height=50)
            self.padding_frame.pack()

            # frame to put the header on
            self.header_frame = Frame(self.root, bg="lightblue")
            self.header_frame.pack()

            # frame to put the sudoku board on
            self.board_canvas = Canvas(self.root, bg="lightblue", bd=0, width=450, height=450, highlightthickness=0, relief='ridge')
            self.board_canvas.pack()

            #frame to put the user's guess info on
            self.user_guess_frame = Frame(self.root, bg="lightblue")
            self.user_guess_frame.pack()

            # frame to put the bottom game info on
            self.user_info_frame = Frame(self.root, bg="lightblue")
            self.user_info_frame.pack()

            #frame to put the buttons on
            self.button_frame = Frame(self.root, bg="lightblue")
            self.button_frame.pack()

            #frame for the escape key message 
            self.escape_message_frame = Frame(self.root, bg="lightblue")
            self.escape_message_frame.pack()



        # Initialize all of the Label widgets
        def initialize_labels(self):
            self.welcome_message = Label(self.header_frame)
            self.welcome_sub_message = Label(self.header_frame)

            self.nums_left_label = Label(self.user_info_frame)
            self.lives_left_label = Label(self.user_info_frame)

            self.user_guessed_label = Label(self.user_guess_frame, text="", bg="lightblue")
            self.user_guessed_label.grid(row=4, column=9)



        # Initialize all of the Button widgets
        def initialize_buttons(self):
            # button to restart the current game
            self.restart_button = Button(self.button_frame, text="Restart", height=2, width=8, font="default 14 bold", command=self.restartGame)
            self.restart_button.grid(row=0, column=0)

            # button to start a new game
            self.new_game_button = Button(self.button_frame, text="New Game", height=2, width=9, font="default 14 bold", command=newGame)
            self.new_game_button.grid(row=0, column=2)

            # button to quit the application
            self.quit_button = Button(self.button_frame, text="Quit", height=2, width=8, font="default 14 bold", command=self.root.destroy)
            self.quit_button.grid(row=0, column=4)

            # padding in between the buttons
            self.button_padding_1 = Label(self.button_frame, text="                      ", bg="lightblue")
            self.button_padding_1.grid(row=0, column=1)
            self.button_padding_2 = Label(self.button_frame, text="                      ", bg="lightblue")
            self.button_padding_2.grid(row=0, column=3)
        


        # Initialize and generate the puzzle and its solution
        def generate_board(self):
            if (self.mode == "easy"):
                    self.sudoku_generator = sudoku_generator.SudokuGenerator(37)
            elif (self.mode == "medium"):
                self.sudoku_generator = sudoku_generator.SudokuGenerator(27)
            elif (self.mode == "hard"):
                self.sudoku_generator = sudoku_generator.SudokuGenerator(19)
            else:
                self.sudoku_generator = sudoku_generator.SudokuGenerator(17)

            self.board = self.sudoku_generator.get_puzzle()
            self.original = copy.deepcopy(self.board) # used when the user restarts the game
            self.board_copy = copy.deepcopy(self.board)
                        
            if(sudoku_solver.solve(self.board_copy)):
                sudoku_solver.solve(self.board_copy)
                self.solution = self.board_copy
            else:
                raise Exception('Error: This board cannot be solved.')




        # Draws the initial board
        def draw_canvas(self):
            # Set up the header
            self.welcome_message = Label(self.header_frame, text="WELCOME TO SUDOKU!", font="Courier 35 bold", bg="lightblue")
            self.welcome_message.grid(row=0, column=9)

            self.welcome_sub_message = Label(self.header_frame, text="Enter a number to make a guess.", bg="lightblue")
            self.welcome_sub_message.config(font=("", 20))
            self.welcome_sub_message.grid(row=1, column=9)

            # Set up the Sudoku board
            self.draw_board()

            # Set up the numbers left and lives left information
            self.display_nums_left()
            self.display_lives_left()
        


        # Draws the sudoku board
        def draw_board(self):

            self.draw_dividers()

            y = 15

            for i in range(9):
                x = 7
                for j in range(9):
                    # If the current space is solved, make it a label
                    if(self.board[i][j] != 0): 
                        # create a label with the sudoku value
                        label = Label(self.board_canvas, text=str(self.board[i][j]), width=2, bd=1, background="PaleGreen1", relief='solid', font="default 18 bold")
                        
                        # adds it to the list of labels
                        self.solved += 1

                        # decrease the number left for this value
                        self.nums_left_to_use[self.board[i][j] - 1] -= 1

                        # puts the new label on the grid  
                        label.place(x=x, y=y)
                        x += 50
        

                    # If the current space is unsolved, make it an entry for user input
                    else:
                        sv = StringVar()
                        sv.trace_add('write', lambda *_, var=sv, row=i, col=j: self.check_entry(var, row, col))
                        entry = Entry(self.board_canvas, text=" ", width=2, justify="center", bd=0, textvariable=sv, font="default 18 bold", relief='flat')
                        entry.place(x=x, y=y)
                        x += 50
                        self.entries.append(entry)
                        self.string_vars.append(sv)
                    
                y += 50
        


        # Draws the horizontal dividers
        def draw_dividers(self):
            self.board_canvas.create_line(0, 154, 445, 154, width=5)
            self.board_canvas.create_line(0, 304, 445, 304, width=5)
            self.board_canvas.create_line(147, 5, 147, 450, width=5)
            self.board_canvas.create_line(297, 5, 297, 450, width=5)
        


        # Turns the numbers left to use into a formatted string
        def display_nums_left(self):
            self.nums_left_label.destroy()

            temp = ""
            num = 1
            for val in self.nums_left_to_use:
                if (val > 0):
                    temp += str(num) + "   "
                num += 1

            text = "Numbers Left To Use:  " + temp
            self.nums_left_label = Label(self.user_info_frame, text=text, height=2, bg="lightblue")
            self.nums_left_label.config(font=("", 20))
            self.nums_left_label.grid(row=8, column=9)
        


        # Displays the number of lives left
        def display_lives_left(self):
            self.lives_left_label.destroy()

            text = "Lives Left:  " + str(self.lives)
            self.lives_left_label = Label(self.user_info_frame, text=text, bg="lightblue")
            self.lives_left_label.config(font=("", 20))
            self.lives_left_label.grid(row=7, column=9)



        # Check the user input
        def check_entry(self, var, row, col):
            self.clear_user_guess_label()

            for index, sv in enumerate(self.string_vars):
                if var == sv:
                    value = var.get()
                    if (value == '1' or value == '2' or value == '3' or value == '4' or value == '5' or value == '6' or value == '7' or value == '8' or value == '9'):
                        if int(value) == self.solution[row][col]:
                            self.guessed_correct(row, col, value, index)
                        else:
                            self.guessed_incorrect(value, index)
                    else:
                        self.invalid_input(index)
        


        # Clears the last label containing the info about the user's guess
        def clear_user_guess_label(self):
            self.user_guessed_label.destroy()
            self.user_guessed_label = Label(self.user_guess_frame, text="", bg="lightblue")
            self.user_guessed_label.grid(row=4, column=9)

        

        # Deals with correct user input by turning the 
        # entry into a label with the correct value
        def guessed_correct(self, row, col, value, index):
            x = self.entries[index].winfo_x()
            y = self.entries[index].winfo_y()

            self.entries[index].destroy()

            del self.entries[index]
            del self.string_vars[index]

            self.clear_user_guess_label()

            label = Label(self.board_canvas, text=value, width=2, relief='solid', bd=1, bg="PaleGreen1", font="default 18 bold")
            self.solved += 1
            self.nums_left_to_use[int(value) - 1] -= 1
            label.place(x=x, y=y)

            self.display_nums_left()
            self.check_game_over()


        # Deals with incorrect user input
        def guessed_incorrect(self, value, index):
            self.entries[index].delete(0, END)
            self.user_guessed_label = Label(self.user_guess_frame, text="INCORRECT", fg="red", font="default 20 bold", bg="lightblue")
            self.user_guessed_label.grid(row=4, column=9)
            self.lives -= 1
            self.display_lives_left()
            self.check_game_over()
            
        

        # Deals with invalid user input
        def invalid_input(self, index):
            self.entries[index].delete(0, END)
            self.user_guessed_label = Label(self.user_guess_frame, text="INVALID ENTRY! ENTER A NUMBER (1 - 9)", fg="red", font="default 20 bold", bg="lightblue")
            self.user_guessed_label.grid(row=4, column=9)
        


        # check if the game is over (either user won or lost)
        def check_game_over(self):
            if (self.lives == 0):
                self.board_canvas.destroy()
                self.board_canvas = Canvas(self.root, bg="lightblue", width=450, height=450, bd=0, highlightthickness=0, relief='ridge')
                self.board_canvas.pack()

                self.welcome_sub_message.destroy()
                self.user_guessed_label.destroy()
                self.nums_left_label.destroy()
                self.lives_left_label.destroy()
                self.escape_message.destroy()

                self.game_over_padding = Label(self.escape_message_frame, text="", bg="lightblue")
                self.game_over_padding.pack()

                self.game_over_message = Label(self.user_info_frame, text="GAME OVER :(", height=3, fg="red", font="default 25 bold", bg="lightblue")
                self.game_over_message.grid(row=1, column=9)

                self.draw_dividers()

                y = 15

                for i in range(9):
                    x = 7
                    for j in range(9):
                        label = Label(self.board_canvas, text=str(self.solution[i][j]), width=2, bd=1, relief='solid', bg="snow3", font="default 18 bold")
                        label.place(x=x, y=y)
                        x += 50
                    y += 50
                
            

            elif (self.solved == 81 and self.correct_solution):
                self.board_canvas.destroy()
                self.board_canvas = Canvas(self.root, bg="lightblue", bd=0, width=450, height=450, highlightthickness=0, relief='ridge')
                self.board_canvas.pack()

                self.welcome_sub_message.destroy()
                self.user_guessed_label.destroy()
                self.nums_left_label.destroy()
                self.lives_left_label.destroy()
                self.escape_message.destroy()

                self.game_over_padding = Label(self.escape_message_frame, text="", bg="lightblue")
                self.game_over_padding.pack()

                self.win_message = Label(self.user_info_frame, text="YOU WIN, GOOD JOB!", fg="violet red", font="default 25 bold", bg="lightblue")
                self.win_message.grid(row=4, column=9)

                self.draw_dividers()

                y = 15

                for i in range(9):
                    x = 7
                    for j in range(9):
                        label = Label(self.board_canvas, text=str(self.solution[i][j]), width=2, relief='solid', bd=1, bg="PaleGreen1", font="default 18 bold")
                        label.place(x=x, y=y)
                        x += 50
                    y += 50
            else:
                pass
        


        # Determines if the user's board equals the solution
        def correct_solution(self):
            for i in range(9):
                for j in range(9):
                    if (self.board[i][j] != self.solution[i][j]):
                        return False
            return True
        


        # Exits fullscreen mode when user presses the escape key
        def end_full_screen(self, event=None):
            self.root.attributes("-fullscreen", False)
            return "break"
        


        # Restarts the current game
        def restartGame(self):
            self.destroy_current_canvas()

            self.board = copy.deepcopy(self.original)
            self.initialize_canvas()

            self.lives = 3
            self.entries = []
            self.string_vars = []   
                 
            self.draw_canvas()

            self.solved = self.get_num_solved()
            self.nums_left_to_use = []
            for num in range(1, 10):
                self.nums_left_to_use.append(self.get_num_left_to_use(num))
            
            self.display_nums_left()

            print(self.nums_left_to_use)
            print(self.solved)



        # Destroys the current widgets in order to restart the game
        def destroy_current_canvas(self):
            self.welcome_message.destroy()
            self.welcome_sub_message.destroy()
            self.board_canvas.destroy()
            self.user_guessed_label.destroy()
            self.lives_left_label.destroy()
            self.nums_left_label.destroy()
            self.restart_button.destroy()
            self.quit_button.destroy()
            self.new_game_button.destroy()
            self.escape_message.destroy()
            self.button_padding_1.destroy()
            self.button_padding_2.destroy()
            self.padding_frame.destroy()

            self.header_frame.destroy()
            self.user_guess_frame.destroy()
            self.user_info_frame.destroy()
            self.button_frame.destroy()
            self.escape_message_frame.destroy()

            if (self.lives == 0):
                self.game_over_message.destroy()
                self.game_over_padding.destroy()
            if (self.solved == 81):
                self.win_message.destroy()
                self.game_over_padding.destroy()

        


        # Gets the number of solved cells
        def get_num_solved(self):
            count = 0
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] != 0:
                        count += 1
            return count
        


        # Gets how many more times the given number can be used
        def get_num_left_to_use(self, num):
            count = 0
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == num:
                        count += 1
            return 9 - count




    game = SudokuGame(root, 3)
    root.mainloop()

    


if __name__ == '__main__':
    def newGame():
        root.destroy()
        start()

    start() 

              
