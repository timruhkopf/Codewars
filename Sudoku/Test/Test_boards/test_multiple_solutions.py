import unittest

from Sudoku.Board.MultiSudoku import Sudoku


class MyTestCase(unittest.TestCase):
    """by kata's conventions, multiple solutions raise 'invalid grid' Valueerror"""

    def tearDown(self) -> None:
        with self.assertRaises(ValueError):
            Sudoku(self.problem)


if __name__ == '__main__':
    unittest.main(exit=False)
