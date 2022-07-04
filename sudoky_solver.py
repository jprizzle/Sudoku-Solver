import tkinter as tk
from functools import partial
import os

# --------------------------------------Declare formatting variables----------------------------------------------------
NUMBER_FONT = "Helvetica"
NUMBER_SIZE = 20
PLACED_NUMBER_COLOR = "white"
SOLVED_NUMBER_COLOR = "#FD971F"
PUZZLE_BG_COLOR = "#242526"
WINDOW_BG_COLOR = "#121212"
BUTTON_BG_COLOR = "#404040"
BUTTON_RELIEF = tk.FLAT
DEFAULT_ERROR_TEXT = "Sudoku Solver!"
DEFAULT_ERROR_COLOR = "grey"
ERROR_COLOR = "#ff6969"

# --------------------------------Define functions used by the GUI elements ---------------------------------------------
class GUI:

    # Define function that resets the error label
    @staticmethod
    def reset_error_label():
        lbl_error["text"] = DEFAULT_ERROR_TEXT
        lbl_error["fg"] = DEFAULT_ERROR_COLOR

    # Define function that defines the target cell when clicked, and changes its color
    @staticmethod
    def choose_element(element, event):
        for i in range(9):
            for j in range(9):
                label_to_remove_color = labels[i][j]
                label_to_remove_color["bg"] = PUZZLE_BG_COLOR

        global target
        target = element
        target["bg"] = "#38393b"

    # Declare function that removes the target object
    @staticmethod
    def remove_target():
        global target
        target["bg"] = PUZZLE_BG_COLOR
        del target

    # Define a function that places number in the targeted cell when the number is pressed
    @staticmethod
    def place_number(event):
        GUI.reset_error_label()
        key_pressed = event.char
        try:
            key_int = int(key_pressed)
            target["text"] = "{}".format(key_int)
            target["fg"] = PLACED_NUMBER_COLOR
        except ValueError:
            lbl_error["fg"] = ERROR_COLOR
            lbl_error["text"] = "Only numbers 1-9 can be placed."
        except NameError:
            lbl_error["fg"] = ERROR_COLOR
            lbl_error["text"] = "Select a box to place number."

    # Declare function that clears cell
    @staticmethod
    def clear_number(event):
        target["text"] = ""

    # Declare function that resets the puzzle, bound to "Reset" button
    @staticmethod
    def reset_button():
        for i in range(9):
            for j in range(9):
                label_to_reset = labels[i][j]
                label_to_reset["text"] = ""
                label_to_reset["fg"] = "black"
        GUI.reset_error_label()
        GUI.remove_target()

    # Define help function, bound to "Help" button
    @staticmethod
    def help_button():
        script_dir = os.path.dirname(__file__)
        rel_path = "Help.txt"
        abs_file_path = os.path.join(script_dir, rel_path)
        os.startfile(abs_file_path)

    # Define function that will solve puzzle, bound to the "Solve" button
    @staticmethod
    def solve_button():
        puzzle = Alg.labels_to_array()
        # Check if valid puzzle
        if not Alg.check_if_valid_puzzle(puzzle):
            lbl_error["text"] = "This configuration is not valid."
            lbl_error["fg"] = ERROR_COLOR
            return

        GUI.remove_target()
        GUI.reset_error_label()
        initial_vals = Alg.store_initial_values(puzzle)
        Alg.solve(puzzle)
        Alg.array_to_labels(puzzle)
        for key in initial_vals:
            i, j = initial_vals[key]
            labels[i][j]["fg"] = PLACED_NUMBER_COLOR


# Define class to house functions that are used by the solving algorithm
class Alg:
    # Defining a function that takes the text in each label and transforms it into a 2D array
    @staticmethod
    def labels_to_array():
        puzzle = [[] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                label_to_transfer = labels[i][j]
                if label_to_transfer["text"] == "":
                    puzzle[i].append(0)
                if label_to_transfer["text"] != "":
                    puzzle[i].append(int(label_to_transfer["text"]))
        return puzzle

    # Define function that inserts the puzzle array into the label objects
    @staticmethod
    def array_to_labels(puzzle):
        for i in range(9):
            for j in range(9):
                labels[i][j]["text"] = str(puzzle[i][j])
                labels[i][j]["fg"] = SOLVED_NUMBER_COLOR

    # Define function that stores the initial placed numbers
    @staticmethod
    def store_initial_values(puzzle):
        initial_vals = {}
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] != 0:
                    initial_vals["i{}x{}".format(i, j)] = (i, j)
        return initial_vals

    # Define function that finds an empty cell
    @staticmethod
    def find_empty_cell(puzzle):
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                if puzzle[i][j] == 0:
                    pos = (i, j)
                    return pos
        return False

    # Define function that checks if a specific number in a specific position is valid
    @staticmethod
    def is_valid_num(puzzle, position, number):
        num = number
        row, col = position
        puzzle = puzzle
        valid = True
        if num != 0:
            # Check row
            for j in range(len(puzzle[row])):
                if puzzle[row][j] == num and j != col:
                    valid = False
            # Check column
            for i in range(len(puzzle)):
                if puzzle[i][col] == num and i != row:
                    valid = False
            # Check box
            box_row = row // 3
            box_col = col // 3
            for i in range(3 * box_row, 3 * box_row + 3):
                for j in range(3 * box_col, 3 * box_col + 3):
                    if puzzle[i][j] == num and (i != row and j != col):
                        valid = False
        return valid

    # Define function that checks if the placed numbers represent a valid puzzle
    @staticmethod
    def check_if_valid_puzzle(puzzle):
        valid = True
        for i in range(len(puzzle)):
            for j in range(len(puzzle[i])):
                num = puzzle[i][j]
                pos = (i, j)
                if not Alg.is_valid_num(puzzle, pos, num):
                    valid = False
        return valid

    # Define function that will house the solving algorithm
    @staticmethod
    def solve(puzzle):
        empty_cell = Alg.find_empty_cell(puzzle)
        if not empty_cell:
            return True
        else:
            pos = empty_cell
            row, col = empty_cell

        for val in range(1, 10):
            if Alg.is_valid_num(puzzle, pos, val):
                puzzle[row][col] = val
                if Alg.solve(puzzle):
                    return True
                puzzle[row][col] = 0

        return False


# -------------------------------------Define and handle all GUI objects-------------------------------------------------

# Create window to store elements
window = tk.Tk()
window.title("Sudoku Solver!")
window.configure(bg=WINDOW_BG_COLOR)

# Configure a 3 row 1 column grid
# The top box will store the puzzle, the middle will store the buttons, and the bottom will store error messages
window.columnconfigure(0, weight=1, minsize=450)
window.rowconfigure(0, weight=1, minsize=450)
window.rowconfigure(1, weight=1, minsize=50)
window.rowconfigure(2, weight=1, minsize=10)
window.resizable(False, False)

# Bind key events to window that will place and clear cell
window.bind("<Key>", GUI.place_number)
window.bind("<BackSpace>", GUI.clear_number)

# Create frame object for the puzzle
frm_puzzle = tk.Frame(master=window, bg=PUZZLE_BG_COLOR)
frm_puzzle.grid(row=0, column=0, padx=10, pady=10)
frm_puzzle.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8], weight=1, minsize=50)
frm_puzzle.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8], weight=1, minsize=50)

# Create label object for background photo in puzzle frame
bg = tk.PhotoImage(file="images/puzzle_background_white.png")
lbl_background = tk.Label(master=frm_puzzle, image=bg, bg=PUZZLE_BG_COLOR)
lbl_background.place(x=-2, y=-2, anchor="nw")

# Create frame object for buttons
frm_buttons = tk.Frame(master=window, bg=WINDOW_BG_COLOR)
frm_buttons.grid(row=1, column=0, sticky="nsew")
frm_buttons.rowconfigure(0, weight=1, minsize=20)
frm_buttons.columnconfigure([0, 1, 2], weight=1)

# Create a frame object for error messages
frm_error = tk.Frame(master=window, bg=WINDOW_BG_COLOR)
frm_error.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
frm_error.rowconfigure(0, minsize=10)
frm_error.columnconfigure(0, minsize=450)

# Create 81 label objects for the numbers in the puzzle
labels = [[] for _ in range(9)]

for i in range(9):
    for j in range(9):
        lbl_box = tk.Label(
            master=frm_puzzle,
            text="",
            font=(NUMBER_FONT, NUMBER_SIZE),
            bg=PUZZLE_BG_COLOR,
        )
        lbl_box.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        labels[i].append(lbl_box)

        element = lbl_box
        choose_element_partial = partial(GUI.choose_element, element)
        lbl_box.bind("<Button-1>", choose_element_partial)

# Create solve button object
btn_solve = tk.Button(
    master=frm_buttons,
    text="Solve",
    borderwidth=4,
    bg=BUTTON_BG_COLOR,
    fg="white",
    relief=BUTTON_RELIEF,
    command=GUI.solve_button,
)
btn_solve.grid(row=0, column=0, sticky="nsew", padx=20, pady=5)

# Create reset button object
btn_reset = tk.Button(
    master=frm_buttons,
    text="Reset",
    borderwidth=4,
    bg=BUTTON_BG_COLOR,
    fg="white",
    relief=BUTTON_RELIEF,
    command=GUI.reset_button,
)
btn_reset.grid(row=0, column=1, sticky="nsew", padx=20, pady=5)

# Create help button object
btn_help = tk.Button(
    master=frm_buttons,
    text="Help",
    borderwidth=4,
    bg=BUTTON_BG_COLOR,
    fg="white",
    relief=BUTTON_RELIEF,
    command=GUI.help_button,
)
btn_help.grid(row=0, column=2, sticky="nsew", padx=20, pady=5)

# Create label object for error messages
lbl_error = tk.Label(
    master=frm_error,
    text=DEFAULT_ERROR_TEXT,
    fg=DEFAULT_ERROR_COLOR,
    bg=PUZZLE_BG_COLOR,
    relief=tk.SOLID,
)
lbl_error.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Start the window
window.mainloop()
