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

    def test_edgepattern(self):
        # top left can be opened safely, since the two ones guarantee it
        # (reduce the factual state of 2 -
        self.result = """
        ? ? ?
        ? 2 1
        ? 1 0
        """

        solution, m = prep_test(self)
        Strategy_Superset.double(m)
        Strategy_Superset.triple(m)

        self.assertEqual(m.board, board(self.result))

    def test_121pattern(self):
        self.result = """
        0 0 0
        1 2 1
        x 2 x
        """

        solution, m = prep_test(self)
        Strategy_Superset.double(m)
        Strategy_Superset.triple(m)

        self.assertEqual(m.board, board(self.result))

    def do_not_find_endgame_bomb(self):
        """Supersets double has a bug, that marks (0,3) correctly as bomb,
        despite this should not be possible for double strategy. (solution is
        endgame combinations)"""
        self.result = """
           0 1 x x 1
           0 1 3 4 3
           0 0 1 x x
           0 0 1 2 2
           0 0 1 1 1
           0 1 2 x 1
           0 1 x 2 1
           """

        solution, m = prep_test(self)

        Strategy_Superset.double(m)  # Fixme: it finds a bomb which it shouldn't

        self.assertEqual(  # equivalent to the zero open calls!
            m.board, board("""
             0 1 x ? ?
             0 1 3 ? ?
             0 0 1 ? ?
             0 0 1 ? ?
             0 0 1 ? ?
             0 1 2 ? ?
             0 1 x ? ?"""))


if __name__ == '__main__':
    unittest.main()
