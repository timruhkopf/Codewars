import unittest

from .Util_tests import Util_tests


class Test_Skyskraper4x4(Util_tests, unittest.TestCase):

    def test_4x4_1(self):
        self.clues = (2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3)
        self.solution = ((1, 3, 4, 2),
                         (4, 2, 1, 3),
                         (3, 4, 2, 1),
                         (2, 1, 3, 4))

    def test_4x4_2(self):
        self.clues = (0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0)
        self.solution = ((2, 1, 4, 3),
                         (3, 4, 1, 2),
                         (4, 2, 3, 1),
                         (1, 3, 2, 4))

    def test_4x4_3(self):
        self.clues = [1, 2, 4, 2, 2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1]
        self.solution = ((4, 2, 1, 3),
                         (3, 1, 2, 4),
                         (1, 4, 3, 2),
                         (2, 3, 4, 1))

    def test_4x4_4(self):
        self.clues = [2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]
        self.solution = ((3, 4, 2, 1),
                         (1, 2, 3, 4),
                         (2, 1, 4, 3),
                         (4, 3, 1, 2))


if __name__ == '__main__':
    unittest.main()
