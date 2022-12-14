"""Unit tests for Cell Module"""
import unittest
from cell import Cell


class TestCell(unittest.TestCase):
    """Class for testing Cell Module"""

    def test_default_cell_instance(self):
        """Test default Cell Instance"""
        cell = Cell(1, 2)
        self.assertEqual(cell.row_nr, 1)
        self.assertEqual(cell.column_nr, 2)
        self.assertFalse(cell.is_open)
        self.assertEqual(cell.nr_neighbor_mines, 0)
        self.assertFalse(cell.is_mine)
        self.assertEqual(len(cell.neighbors), 0)

    def test_get_display_value_for_non_open_mine_cell(self):
        """Test get display function for non open mine cell"""
        cell = Cell(1, 1)
        cell.is_mine = True
        cell.nr_neighbor_mines = 3
        self.assertEqual(cell.get_display_value(), '-')

    def test_get_display_value_for_non_open_cell(self):
        """Test get display function for non open non mine cell"""
        cell = Cell(1, 1)
        cell.nr_neighbor_mines = 3
        self.assertEqual(cell.get_display_value(), '-')

    def test_get_display_value_for_open_mine_cell(self):
        """Test get display function for open mine cell"""
        cell = Cell(1, 1)
        cell.is_mine = True
        cell.is_open = True
        cell.nr_neighbor_mines = 3
        self.assertEqual(cell.get_display_value(), 'M')

    def test_get_display_value_for_open_non_mine_cell(self):
        """Test get display function for open cell"""
        cell = Cell(1, 1)
        cell.nr_neighbor_mines = 3
        cell.is_open = True
        self.assertEqual(cell.get_display_value(), '3')


if __name__ == '__main__':
    unittest.main()
