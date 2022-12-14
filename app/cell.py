"""Cell Module File"""


class Cell:
    """Class to represent a cell in the board"""

    def __init__(self, row_nr, column_nr):
        self.row_nr = row_nr
        self.column_nr = column_nr
        self.is_open = False
        self.nr_neighbor_mines = 0
        self.is_mine = False
        self.neighbors = []  # Array of neighbor cells

    # Gets the cell value to be displayed when printing the board
    def get_display_value(self):
        """Get the cell value to be displayed, in string format."""
        if not self.is_open:
            return '-'
        if self.is_mine:
            return 'M'
        return str(self.nr_neighbor_mines)

    def set_neighbors(self, neighbors):
        """Sets the neighbors for the cell"""
        self.neighbors = neighbors
