import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Strategies import Strategy_Superset
from ..Util import board


def prep_test(self):
    """tearDown like method, that sets up the basic test enviroment of the board"""
    solution = Solution(board(self.result))
    m = Game(board=solution.covered_board, n=solution.n, context=solution)

    # opening a single zero suffices to recursively communicate ('open') all zeros
    # & remove them from m.zeros entirely
    while bool(m.zeros):
        zero = m.zeros.pop()
        m.open(*zero)

        placedzeros = set(n.position for n in m.clues.values() if n.clue == 0)
        m.zeros.difference_update(placedzeros)

    return solution, m


class TestSupersets(unittest.TestCase):

    def test_121pattern(self):
        self.result = """
        0 0 0
        1 2 1
        x 2 x
        """

        solution, m = prep_test(self)
        Strategy_Superset.tripple(m)


if __name__ == '__main__':
    unittest.main()
