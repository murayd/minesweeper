"""Board Module File"""
from random import randint
from enum import Enum
from cell import Cell


class BoardState(Enum):
    """Constants for Board States"""
    NO_MINE_OPEN_SOME_NON_MINE_CLOSED = 0
    A_MINE_OPEN = 1
    ALL_NON_MINE_OPEN = 2


class Board:
    """Class to represent a board"""

    def __init__(self, nr_rows, nr_columns, nr_mines):
        self.nr_rows = nr_rows
        self.nr_columns = nr_columns
        self.nr_mines = nr_mines
        self.nr_open_non_mine_cells = 0
        self.state = BoardState.NO_MINE_OPEN_SOME_NON_MINE_CLOSED
        # Array of Array of cells, Example:
        # [
        #   [Cell(1,1), Cell(1,2), ...],
        #   [Cell(2,1), Cell(2,2), ...],
        #   ...
        # ]
        self.cells = []
        self.__populate()

    def reset(self, nr_rows, nr_columns, nr_mines):
        """Resets the board with new settings and populates with cells and mines"""
        self.nr_rows = nr_rows
        self.nr_columns = nr_columns
        self.nr_mines = nr_mines
        self.nr_open_non_mine_cells = 0
        self.state = BoardState.NO_MINE_OPEN_SOME_NON_MINE_CLOSED
        self.cells = []
        self.__populate()
        return self

    def __get_cell(self, row_nr, column_nr):
        # TODO(handle exception): Check that passed indexes are within range
        return self.cells[row_nr][column_nr]

    def is_coordinates_within_range(self, row_nr, column_nr):
        """Checks if the coordinate corresponding to given (row_nr, column_nr) in the board"""
        return self.nr_rows > row_nr >= 0 and self.nr_columns > column_nr >= 0

    def __get_neighbors_cells(self, cell):
        """Gets neighbors of a given cell"""
        row_nr = cell.row_nr
        column_nr = cell.column_nr
        # A cell can have maximum 8 neighbors
        coordinates = [[row_nr - 1, column_nr - 1], [row_nr - 1, column_nr],
                       [row_nr - 1, column_nr + 1], [row_nr, column_nr - 1],
                       [row_nr, column_nr + 1], [row_nr + 1, column_nr - 1],
                       [row_nr + 1, column_nr], [row_nr + 1, column_nr + 1]]

        # Then we eleminate the coordinates that goes outside of the board
        neighbor_coordinates = [[row_nr, column_nr] for [row_nr, column_nr] in coordinates
                                if self.is_coordinates_within_range(row_nr, column_nr)]
        neighbors = []
        for [neighbor_row_nr, neighbor_column_nr] in neighbor_coordinates:
            neighbor = self.__get_cell(neighbor_row_nr, neighbor_column_nr)
            neighbors.append(neighbor)
        return neighbors

    def __iterate_cells(self, callback):
        for row_nr in range(self.nr_rows):
            for column_nr in range(self.nr_columns):
                cell = self.__get_cell(row_nr, column_nr)
                callback(cell)
        return self

    def __init_cells(self):
        """Initializes the cells for the board"""
        # create cells
        self.cells = [[Cell(row_nr, column_nr) for column_nr in range(
            self.nr_columns)] for row_nr in range(self.nr_rows)]

        # establish neighbor relations
        def set_neighbors(cell):
            neighbors = self.__get_neighbors_cells(cell)
            cell.set_neighbors(neighbors)

        return self.__iterate_cells(set_neighbors)

    def __place_mines(self):
        """Places mines in random locations in the board"""
        # create mines
        mine_cells = set()
        while len(mine_cells) < self.nr_mines:
            row_nr = randint(0, self.nr_rows - 1)
            column_nr = randint(0, self.nr_columns - 1)
            cell = self.__get_cell(row_nr, column_nr)
            cell.is_mine = True
            mine_cells.add(cell)

        # update the non-mine neighbors of mine-cells
        for mine_cell in mine_cells:
            for neighbor in mine_cell.neighbors:
                if not neighbor.is_mine:
                    neighbor.nr_neighbor_mines += 1
        return self

    def __populate(self):
        """Populates the board by setting up the cells and placing mines"""
        self.__init_cells()
        self.__place_mines()
        return self

    def __get_cell(self, row_nr, column_nr):
        """Gets a cell from given coordinate"""
        return self.cells[row_nr][column_nr]

    def display(self):
        """Displays the board by printing to the console."""
        printed_frame_top_row_nr = 0
        max_number_with_single_digit = 9
        column_numbers = range(self.nr_columns)
        row_numbers = range(self.nr_rows)

        print()
        print("\t\t\tMinesweeper\n")

        console_line = "   "
        for column_nr in column_numbers:
            if column_nr > max_number_with_single_digit:
                console_line = console_line + "    " + str(column_nr + 1)
            else:
                console_line = console_line + "     " + str(column_nr + 1)
        print(console_line)

        for row_nr in row_numbers:
            console_line = "     "
            if row_nr == printed_frame_top_row_nr:
                for column_nr in column_numbers:
                    console_line = console_line + "______"
                print(console_line)

            console_line = "     "
            for column_nr in column_numbers:
                console_line = console_line + "|     "
            print(console_line + "|")
            if row_nr >= max_number_with_single_digit:
                console_line = " " + str(row_nr + 1) + "  "
            else:
                console_line = "  " + str(row_nr + 1) + "  "
            for column_nr in column_numbers:
                cell = self.__get_cell(row_nr, column_nr)
                console_line = console_line + "|  " + cell.get_display_value() + "  "
            print(console_line + "|")

            console_line = "     "
            for column_nr in column_numbers:
                console_line = console_line + "|_____"
            print(console_line + '|')

        print()
        if self.state != BoardState.A_MINE_OPEN:
            print("Total Number of Mines : " + str(self.nr_mines))

    def open_all_mines(self):
        """Opens all the mines in the board."""
        self.state = BoardState.A_MINE_OPEN

        def open_mine(cell):
            if cell.is_mine:
                cell.is_open = True
        return self.__iterate_cells(open_mine)

    def close_all_mines(self):
        """Closes all the mines in the board."""
        self.state = BoardState.NO_MINE_OPEN_SOME_NON_MINE_CLOSED

        def close_mine(cell):
            if cell.is_mine:
                cell.is_open = False
        return self.__iterate_cells(close_mine)

    def __is_all_non_mine_cells_open(self):
        """Checks if all non-mine cells are open"""
        nr_non_mine_cells = self.nr_columns * self.nr_rows - self.nr_mines
        return self.nr_open_non_mine_cells == nr_non_mine_cells

    def is_cell_open(self, row_nr, column_nr):
        """Checks if a given cell is open"""
        return self.__get_cell(row_nr, column_nr).is_open

    def open_cell(self, row_nr, column_nr):
        """Opens the cell in board which corresponds to (row_nr, column_nr)."""
        cell = self.__get_cell(row_nr, column_nr)

        if cell.is_open:
            return self

        if cell.is_mine:
            self.open_all_mines()
            return self

        # Here cell.nr_neighbor_mines can be 0,1,2,3,4,5,6,7,8
        cell.is_open = True

        self.nr_open_non_mine_cells += 1
        if self.__is_all_non_mine_cells_open():
            self.state = BoardState.ALL_NON_MINE_OPEN
            return self

        if cell.nr_neighbor_mines == 0:
            # Open all non mine neighbors
            for neighbor in cell.neighbors:
                if not neighbor.is_mine:
                    self.open_cell(neighbor.row_nr, neighbor.column_nr)
        return self
