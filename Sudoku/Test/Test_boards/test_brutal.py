import unittest

from Sudoku.Board.MultiSudoku import Sudoku


class MyTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        self.assertEqual(Sudoku(self.problem).solve_single(), self.solution)
        # self.assertEqual(Sudoku(self.problem).solve(), self.solution)

    # def test_sparse2(self):
    #     # Fixme: multiples?
    #     # randomtest:  Fixme killing my time
    #     problem = [[0, 5, 7, 2, 0, 0, 0, 0, 0],
    #                [0, 0, 0, 0, 9, 0, 8, 1, 0],
    #                [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                [0, 0, 0, 0, 0, 0, 0, 9, 4],
    #                [8, 0, 0, 0, 0, 0, 0, 3, 0],
    #                [0, 0, 2, 0, 0, 7, 0, 0, 0],
    #                [9, 0, 0, 0, 3, 0, 0, 0, 0],
    #                [0, 0, 0, 0, 0, 0, 0, 0, 7],
    #                [0, 8, 0, 0, 0, 0, 0, 0, 5]]
    #
    #     # FIXME. does this one have a Solution?
    #     Sudoku(problem).solve()

    def test_sparse(self):
        self.problem = [[0, 0, 0, 0, 0, 2, 7, 5, 0],
                        [0, 1, 8, 0, 9, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [4, 9, 0, 0, 0, 0, 0, 0, 0],
                        [0, 3, 0, 0, 0, 0, 0, 0, 8],
                        [0, 0, 0, 7, 0, 0, 2, 0, 0],
                        [0, 0, 0, 0, 3, 0, 0, 0, 9],
                        [7, 0, 0, 0, 0, 0, 0, 0, 0],
                        [5, 0, 0, 0, 0, 0, 0, 8, 0]]
        # FIXME:THIS CASE seems to be incapable to place any values and incapable of stopping

        self.solution = [[9, 4, 6, 1, 8, 2, 7, 5, 3],
                         [3, 1, 8, 5, 9, 7, 4, 2, 6],
                         [2, 7, 5, 6, 4, 3, 8, 9, 1],
                         [4, 9, 2, 3, 1, 8, 5, 6, 7],
                         [6, 3, 7, 2, 5, 4, 9, 1, 8],
                         [8, 5, 1, 7, 6, 9, 2, 3, 4],
                         [1, 2, 4, 8, 3, 5, 6, 7, 9],
                         [7, 8, 3, 9, 2, 6, 1, 4, 5],
                         [5, 6, 9, 4, 7, 1, 3, 8, 2]]

    def test_sparse3(self):
        self.problem = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 3, 6, 0, 0, 0, 0, 0],
                        [0, 7, 0, 0, 9, 0, 2, 0, 0],
                        [0, 5, 0, 0, 0, 7, 0, 0, 0],
                        [0, 0, 0, 0, 4, 5, 7, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 3, 0],
                        [0, 0, 1, 0, 0, 0, 0, 6, 8],
                        [0, 0, 8, 5, 0, 0, 0, 1, 0],
                        [0, 9, 0, 0, 0, 0, 4, 0, 0]]

        self.solution = [[8, 1, 2, 7, 5, 3, 6, 4, 9],
                         [9, 4, 3, 6, 8, 2, 1, 7, 5],
                         [6, 7, 5, 4, 9, 1, 2, 8, 3],
                         [1, 5, 4, 2, 3, 7, 8, 9, 6],
                         [3, 6, 9, 8, 4, 5, 7, 2, 1],
                         [2, 8, 7, 1, 6, 9, 5, 3, 4],
                         [5, 2, 1, 9, 7, 4, 3, 6, 8],
                         [4, 3, 8, 5, 2, 6, 9, 1, 7],
                         [7, 9, 6, 3, 1, 8, 4, 5, 2]]


if __name__ == '__main__':
    unittest.main()
