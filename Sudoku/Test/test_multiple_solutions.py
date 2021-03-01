import unittest

from Sudoku.Board.MultiSudoku import Sudoku


class MyTestCase(unittest.TestCase):
    """by kata's conventions, multiple solutions raise 'invalid grid' Valueerror"""

    def tearDown(self) -> None:
        s = Sudoku(self.problem)
        # solve should raise, since kata requires it is invalid; however, solutions are appended when found
        # changing the Sudoku object!
        with self.assertRaises(ValueError):
            s.solve()
        # self.assertTrue(len(s.solutions) > 1)
        for sol in s.solutions:
            self.assertTrue(sol in self.solutions)

    def test_square_switch(self):
        """the two solutions are almost identical; except a switch in row 5 & 6"""
        self.problem = [[9, 0, 6, 0, 7, 0, 4, 0, 3],
                        [0, 0, 0, 4, 0, 0, 2, 0, 0],
                        [0, 7, 0, 0, 2, 3, 0, 1, 0],
                        [5, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 4, 0, 2, 0, 8, 0, 6, 0],
                        [0, 0, 3, 0, 0, 0, 0, 0, 5],
                        [0, 3, 0, 7, 0, 0, 0, 5, 0],
                        [0, 0, 7, 0, 0, 5, 0, 0, 0],
                        [4, 0, 5, 0, 1, 0, 7, 0, 8]]

        self.solutions = [
            [[9, 2, 6, 5, 7, 1, 4, 8, 3],
             [3, 5, 1, 4, 8, 6, 2, 7, 9],
             [8, 7, 4, 9, 2, 3, 5, 1, 6],
             [5, 8, 2, 3, 6, 7, 1, 9, 4],
             [1, 4, 9, 2, 5, 8, 3, 6, 7],
             [7, 6, 3, 1, 9, 4, 8, 2, 5],  # 9, 4
             [2, 3, 8, 7, 4, 9, 6, 5, 1],  # 4, 9
             [6, 1, 7, 8, 3, 5, 9, 4, 2],
             [4, 9, 5, 6, 1, 2, 7, 3, 8]],

            [[9, 2, 6, 5, 7, 1, 4, 8, 3],
             [3, 5, 1, 4, 8, 6, 2, 7, 9],
             [8, 7, 4, 9, 2, 3, 5, 1, 6],
             [5, 8, 2, 3, 6, 7, 1, 9, 4],
             [1, 4, 9, 2, 5, 8, 3, 6, 7],
             [7, 6, 3, 1, 4, 9, 8, 2, 5],  # 4, 9
             [2, 3, 8, 7, 9, 4, 6, 5, 1],  # 9, 4
             [6, 1, 7, 8, 3, 5, 9, 4, 2],
             [4, 9, 5, 6, 1, 2, 7, 3, 8]]
        ]


if __name__ == '__main__':
    unittest.main(exit=False)
