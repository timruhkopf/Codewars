import unittest

from ..Util import solve_puzzle


class Test_Skyscraper7x7_ambigious(unittest.TestCase):
    def test_7x7_1(self):
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
    unittest.main()
