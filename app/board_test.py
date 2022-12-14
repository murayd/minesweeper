"""Unit tests for Board Module"""
import unittest
from board import Board, BoardState

# Run tests with default board
NR_ROWS = 8
NR_COLUMNS = 8
NR_MINES = 10


class TestBoard(unittest.TestCase):
    """Class for testing Board Module"""

    def test_default_board_instance(self):
        """Test default Board Instance"""
        board = Board(NR_ROWS, NR_COLUMNS, NR_MINES)
        self.assertEqual(board.nr_rows, NR_ROWS)
        self.assertEqual(board.nr_columns, NR_COLUMNS)
        self.assertEqual(board.nr_mines, NR_MINES)
        self.assertEqual(board.nr_mines, NR_MINES)
        self.assertEqual(len(board.cells), NR_ROWS)
        self.assertEqual(
            board.state, BoardState.NO_MINE_OPEN_SOME_NON_MINE_CLOSED)
        self.assertEqual(board.nr_open_non_mine_cells, 0)


if __name__ == '__main__':
    unittest.main()
