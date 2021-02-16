import unittest

from ..Solver import Skyscraper


class Test_viability(unittest.TestCase):
    def test_visability4x4(self):
        tests = {1: [(4, 3, 2, 1), (4, 1, 2, 3)],
                 3: [(2, 3, 1, 4), (1, 2, 4, 3)],
                 4: [(1, 2, 3, 4)]}

        for tups, visable in tests.items():
            for tup in tups:
                self.assertEqual(Skyscraper._visible(tup), visable)

    def test_visability7x7(self):
        tests = {1: [(7, 6, 5, 4, 3, 2, 1), (7, 4, 3, 5, 6, 1, 2)],
                 3: [(2, 5, 7, 1, 3, 4, 6), (4, 6, 7, 1, 2, 3, 5)],
                 7: [(1, 2, 3, 4, 5, 6, 7)]}

        for tups, visable in tests.items():
            for tup in tups:
                self.assertEqual(Skyscraper._visible(tup), visable)

    def test_sort_permutations(self):
        self.assertEqual(True, False)

    def test_interpret_clues(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
