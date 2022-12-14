"""Main module for MineSweeper Game"""
import os
import sys
from board import Board, BoardState

NR_INPUT_TO_DEFINE_A_COORDINATE = 2

game_modes = {"Beginner": {"NR_ROWS": 8, "NR_COLUMNS": 8, "NR_MINES": 10},
              "Intermediate": {"NR_ROWS": 12, "NR_COLUMNS": 12, "NR_MINES": 30},
              "Expert": {"NR_ROWS": 16, "NR_COLUMNS": 16, "NR_MINES": 40}}

# Messages
WRONG_INPUT_MESSAGE = "\n\n****** Wrong input! ******\n\n"
REQUEST_CELL_TO_OPEN_PROMPT = ("Enter row and column numbers with a space in between "
                               "( example: 1 1), to quit enter Q :  ")
CHOOSE_GAME_MODE_PROMPT = ("Please choose a game mode.Empty Enter for default, "
                           "Enter B for beginner, I for intermediate and E for expert,"
                           " to quit enter Q: ")
GAME_MODE_OPTIONS = ("B", "I", "E", "")
INSTRUCTION_TO_PLAY = ("Enter row and column number to select a cell, Example \"2 3\"."
                       " After entering that Cell will be opened. "
                       "You can enter Q at any prompt to quit")
ALREADY_OPENED_CELL_MESSAGE = "\n\nChosen cell is already Open, please enter a non-open Cell!"
LOST_MESSAGE = "Sorry, You opened a Mine and Lost!"
LOST_PROMPT = ("\nEnter C to continue where you were left, "
               "R to start a completely new game or Q to quit:  ")
WON_MESSAGE = "Congrats, You Won!!!"
WON_PROMPT = "\nEnter R to start a completely new game or Q to quit: "


def clear():
    """Clears the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def is_game_over(board):
    """Checks if game over condition is reached"""
    return board.state == BoardState.A_MINE_OPEN


def is_game_continue(board):
    """Checks if game should continue"""
    return board.state == BoardState.NO_MINE_OPEN_SOME_NON_MINE_CLOSED


def is_game_won(board):
    """Checks if game won condition is reached"""
    return board.state == BoardState.ALL_NON_MINE_OPEN


def handle_wrong_input():
    """Function to handle wrong input"""
    clear()
    print(WRONG_INPUT_MESSAGE)


def valid_coordinate_input(user_input):
    """Checks if given input is a valid coordinate"""
    return len(user_input) == NR_INPUT_TO_DEFINE_A_COORDINATE


def shoud_exit(user_input):
    """Exits with sys exit if user enter Q"""
    if user_input.upper() == "Q":
        sys.exit("Quit Detected")


def map_user_input_to_game_mode(user_input):
    """Convert user input to Game mode"""
    default_game_mode = "Beginner"

    if user_input == "B":
        return "Beginner"
    if user_input == "I":
        return "Intermediate"
    if user_input == "E":
        return "Expert"
    return default_game_mode


if __name__ == "__main__":
    GAME_MODE_CHOSEN = False
    GAME_OVER = False

    clear()

    while not GAME_OVER:

        if not GAME_MODE_CHOSEN:
            # Get game mode from user
            IS_INPUT_VALID = False
            while not IS_INPUT_VALID:
                game_mode_input = input(
                    CHOOSE_GAME_MODE_PROMPT).strip().upper()
                shoud_exit(game_mode_input)
                if game_mode_input in GAME_MODE_OPTIONS:
                    IS_INPUT_VALID = True
                else:
                    print(WRONG_INPUT_MESSAGE)

            GAME_MODE = map_user_input_to_game_mode(game_mode_input)
            nr_rows = game_modes[GAME_MODE].get("NR_ROWS")
            nr_columns = game_modes[GAME_MODE].get("NR_COLUMNS")
            nr_mines = game_modes[GAME_MODE].get("NR_MINES")
            game_board = Board(nr_rows, nr_columns, nr_mines)
            GAME_MODE_CHOSEN = True
            clear()

        print(INSTRUCTION_TO_PLAY)
        game_board.display()
        user_coordinates_input = input(REQUEST_CELL_TO_OPEN_PROMPT).strip()
        shoud_exit(user_coordinates_input)
        user_coordinates = user_coordinates_input.split()
        if not valid_coordinate_input(user_coordinates):
            handle_wrong_input()
            continue
        try:
            chosen_coordinates = list(map(int, user_coordinates))
        except ValueError:
            handle_wrong_input()
            continue
        row_nr = chosen_coordinates[0] - 1
        column_nr = chosen_coordinates[1] - 1
        chosen_coordinates_within_range = game_board.is_coordinates_within_range(
            row_nr, column_nr)

        if not chosen_coordinates_within_range:
            handle_wrong_input()
            continue

        if game_board.is_cell_open(row_nr, column_nr):
            clear()
            print(ALREADY_OPENED_CELL_MESSAGE)
            continue
        game_board.open_cell(row_nr, column_nr)
        if is_game_continue(game_board):
            clear()
            continue
        if is_game_over(game_board):
            clear()
            game_board.display()
            print(LOST_MESSAGE)
            IS_INPUT_VALID = False
            while not IS_INPUT_VALID:
                user_command_on_loss = input(LOST_PROMPT).strip().upper()
                shoud_exit(user_command_on_loss)
                if user_command_on_loss in ("C", "R"):
                    IS_INPUT_VALID = True
                else:
                    print(WRONG_INPUT_MESSAGE)
            if user_command_on_loss == "C":
                game_board.close_all_mines()
                clear()
                continue
            if user_command_on_loss == "R":
                GAME_MODE_CHOSEN = False
                clear()
                continue
        elif is_game_won(game_board):
            game_board.open_all_mines()
            clear()
            game_board.display()
            print(WON_MESSAGE)
            IS_INPUT_VALID = False
            while not IS_INPUT_VALID:
                user_command_on_win = input(WON_PROMPT).strip().upper()
                shoud_exit(user_command_on_win)
                if user_command_on_win == "R":
                    IS_INPUT_VALID = True
                else:
                    print(WRONG_INPUT_MESSAGE)
            if user_command_on_win == "R":
                GAME_MODE_CHOSEN = False
                clear()
                continue
        clear()
