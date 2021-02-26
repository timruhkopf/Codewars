import unittest

from Skyscraper7x7.Solver.Solver import Skyscraper
from Skyscraper7x7.Strategies.StrategyStack import StrategyStack


class MyTestCase(unittest.TestCase):
    """StrategyStack is a full fledged solver on its own (but inefficent if the
    number of choices becomes large)"""

    def tearDown(self):
        sky = Skyscraper(self.clues)
        sky.downtown_row = {r: list(sky.pclues[sky.rowclues[r]]) for r in range(sky.probsize)}
        sky.downtown_col = {c: list(sky.pclues[sky.colclues[c]]) for c in range(sky.probsize)}
        StrategyStack.execute(sky)

        provided = tuple(tuple(sky.downtown_row[i][0]) for i in range(sky.probsize))

        self.assertEqual(self.solution, provided)

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
    unittest.main(exit=False)
