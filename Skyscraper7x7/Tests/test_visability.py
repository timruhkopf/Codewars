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
        # check id of the reversed tuples is indeed the same (memory efficiency)
        pass
        # self.assertEqual(True, False)

    def test_consecutive_solving(self):
        """consecutive solving calls do invoke sort_permutations only once."""

        def count_calls(func):
            count_calls.calls = 0

            def wrapper(self, *args):
                count_calls.calls += 1
                return func(self)

            return wrapper

        Skyscraper._sort_permutations = count_calls(Skyscraper._sort_permutations)

        sky1 = Skyscraper((2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3))
        self.assertEqual(sky1.solve(),
                         ((1, 3, 4, 2),
                          (4, 2, 1, 3),
                          (3, 4, 2, 1),
                          (2, 1, 3, 4)))

        sky2 = Skyscraper((0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0))
        self.assertEqual(sky2.solve,
                         ((2, 1, 4, 3),
                          (3, 4, 1, 2),
                          (4, 2, 3, 1),
                          (1, 3, 2, 4)))

        # TODO check if count of calls works appropriately
        self.assertEqual(Skyscraper._sort_permutations.calls, 1)

    def test_interpret_clues(self):
        pass
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
