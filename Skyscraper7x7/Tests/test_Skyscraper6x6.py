import unittest

from .Util_tests import Util_tests


class test_Skyscraper6x6(Util_tests, unittest.TestCase):

    def test_6x6_1(self):
        self.clues = (0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0)
        self.solution = ((5, 6, 1, 4, 3, 2),
                         (4, 1, 3, 2, 6, 5),
                         (2, 3, 6, 1, 5, 4),
                         (6, 5, 4, 3, 2, 1),
                         (1, 2, 5, 6, 4, 3),
                         (3, 4, 2, 5, 1, 6))

    def test_6x6_2(self):
        self.clues = (3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3, 3, 2, 1, 2, 2, 4)
        self.solution = ((2, 1, 4, 3, 5, 6),
                         (1, 6, 3, 2, 4, 5),
                         (4, 3, 6, 5, 1, 2),
                         (6, 5, 2, 1, 3, 4),
                         (5, 4, 1, 6, 2, 3),
                         (3, 2, 5, 4, 6, 1))

    def test_6x6_3(self):
        self.clues = (0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0)
        self.solution = ((5, 2, 6, 1, 4, 3),
                         (6, 4, 3, 2, 5, 1),
                         (3, 1, 5, 4, 6, 2),
                         (2, 6, 1, 5, 3, 4),
                         (4, 3, 2, 6, 1, 5),
                         (1, 5, 4, 3, 2, 6))


if __name__ == '__main__':
    unittest.main(exit=False)
