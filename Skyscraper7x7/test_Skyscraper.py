# # tutorial on how to write unittests
# # https://realpython.com/python-testing/#writing-your-first-test
import unittest

from Skyscraper7x7.Skyscraper7x7 import solve_puzzle
from Skyscraper7x7.helper_Interpretation import _interpret_clues


class Test_Skyscraper(unittest.TestCase):
    # TODO test permutations & visibility

    def test_clueparsing(self):
        self.assertEqual(_interpret_clues(tuple(i for i in range(1, 17)), probsize=4)[0],
                         [(1, 12), (2, 11), (3, 10), (4, 9)], 'Tested colclues')
        self.assertEqual(_interpret_clues(tuple(i for i in range(1, 17)), probsize=4)[1],
                         [(16, 5), (15, 6), (14, 7), (13, 8)], 'Tested colclues')

    def test_skyscraper4x4(self):
        self.assertEqual(solve_puzzle((2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3)), \
                         ((1, 3, 4, 2),
                          (4, 2, 1, 3),
                          (3, 4, 2, 1),
                          (2, 1, 3, 4)))

        self.assertEqual(solve_puzzle((0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0)), \
                         ((2, 1, 4, 3),
                          (3, 4, 1, 2),
                          (4, 2, 3, 1),
                          (1, 3, 2, 4)))

        self.assertEqual(solve_puzzle([1, 2, 4, 2, 2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1]), \
                         ((4, 2, 1, 3),
                          (3, 1, 2, 4),
                          (1, 4, 3, 2),
                          (2, 3, 4, 1)))

        self.assertEqual(solve_puzzle([2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]), \
                         ((3, 4, 2, 1),
                          (1, 2, 3, 4),
                          (2, 1, 4, 3),
                          (4, 3, 1, 2)))

    def test_skyscraper6x6(self):
        self.assertEqual(
            solve_puzzle((0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0)),
            ((5, 6, 1, 4, 3, 2),
             (4, 1, 3, 2, 6, 5),
             (2, 3, 6, 1, 5, 4),
             (6, 5, 4, 3, 2, 1),
             (1, 2, 5, 6, 4, 3),
             (3, 4, 2, 5, 1, 6)))

        self.assertEqual(
            solve_puzzle((3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3, 3, 2, 1, 2, 2, 4)),
            ((2, 1, 4, 3, 5, 6),
             (1, 6, 3, 2, 4, 5),
             (4, 3, 6, 5, 1, 2),
             (6, 5, 2, 1, 3, 4),
             (5, 4, 1, 6, 2, 3),
             (3, 2, 5, 4, 6, 1)))

        self.assertEqual(
            solve_puzzle((0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0)),
            ((5, 2, 6, 1, 4, 3),
             (6, 4, 3, 2, 5, 1),
             (3, 1, 5, 4, 6, 2),
             (2, 6, 1, 5, 3, 4),
             (4, 3, 2, 6, 1, 5),
             (1, 5, 4, 3, 2, 6)))

    def test_skyscraper7x7(self):
        self.assertEqual(
            solve_puzzle([3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3]), \
            [[2, 1, 4, 7, 6, 5, 3],
             [6, 4, 7, 3, 5, 1, 2],
             [1, 2, 3, 6, 4, 7, 5],
             [5, 7, 6, 2, 3, 4, 1],
             [4, 3, 5, 1, 2, 6, 7],
             [7, 6, 2, 5, 1, 3, 4],
             [3, 5, 1, 4, 7, 2, 6]])


if __name__ == '__main__':
    unittest.main(exit=False)
