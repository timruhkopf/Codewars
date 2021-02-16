import unittest

from ..Util import solve_puzzle


class Test_Skyskraper4x4(unittest.TestCase):

    def test_4x4_1(self):
        self.assertEqual(solve_puzzle((2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3)), \
                         ((1, 3, 4, 2),
                          (4, 2, 1, 3),
                          (3, 4, 2, 1),
                          (2, 1, 3, 4)))

    def test_4x4_2(self):
        self.assertEqual(solve_puzzle((0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0)), \
                         ((2, 1, 4, 3),
                          (3, 4, 1, 2),
                          (4, 2, 3, 1),
                          (1, 3, 2, 4)))

    def test_4x4_3(self):
        self.assertEqual(solve_puzzle([1, 2, 4, 2, 2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1]), \
                         ((4, 2, 1, 3),
                          (3, 1, 2, 4),
                          (1, 4, 3, 2),
                          (2, 3, 4, 1)))

    def test_4x4_4(self):
        self.assertEqual(solve_puzzle([2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]), \
                         ((3, 4, 2, 1),
                          (1, 2, 3, 4),
                          (2, 1, 4, 3),
                          (4, 3, 1, 2)))


if __name__ == '__main__':
    unittest.main()
