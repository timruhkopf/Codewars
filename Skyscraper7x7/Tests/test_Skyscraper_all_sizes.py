import unittest

from ..Util import solve_puzzle


class TestSkyscraper(unittest.TestCase):
    def test_4x4_4(self):
        self.assertEqual(
            solve_puzzle([2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]), \
            ((3, 4, 2, 1),
             (1, 2, 3, 4),
             (2, 1, 4, 3),
             (4, 3, 1, 2)))

    def test_6x6_1(self):
        self.assertEqual(
            solve_puzzle((0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0)),
            ((5, 6, 1, 4, 3, 2),
             (4, 1, 3, 2, 6, 5),
             (2, 3, 6, 1, 5, 4),
             (6, 5, 4, 3, 2, 1),
             (1, 2, 5, 6, 4, 3),
             (3, 4, 2, 5, 1, 6)))

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
    unittest.main()
