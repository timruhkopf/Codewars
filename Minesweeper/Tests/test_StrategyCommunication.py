import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Util import board


# TODO remain_bomb_count cases fail after considering only solve()'s snipped opening the zeros.
# TODO make more atomic tests on updating to ensure the behaviour is correct and
#  check that after a discard ? or statechange a ceck up on the conditions is done appropriately
class TestMinesweeperSolvables(unittest.TestCase):

    def tearDown(self) -> None:
        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)

        count = 0
        while bool(m.zeros):
            zero = m.zeros.pop()
            m.open(*zero)

            placedzeros = set(n.position for n in m.clues.values() if n.clue == 0)
            m.zeros.difference_update(placedzeros)
            count += 1

        self.assertEqual(count, 1)
        self.assertEqual(m.board, board(self.result))

        del self.result

    def test_CommunicationSimple0(self):
        self.result = """
        1 x 1 0
        1 1 1 0
        0 0 0 0
        """

    def test_CommunicationSimple0transpose(self):
        """partial of Com.Strategy 1: only com. strategy is required to solve the board."""
        self.result = """
        0 0 0
        0 1 1
        0 1 x
        0 1 1
        """

    def test_CommunicationPartial1(self):
        self.result = """
        0 2 x 2 1 x 1 0
        0 2 x 3 2 1 1 0
        0 1 2 x 1 0 0 0
        0 0 1 1 1 0 0 0
        0 0 0 0 0 0 0 0
        """

    def test_CommunicationStrategy01(self):
        """simplified partial of Com.Strategy 1: only com. strategy is required to solve the board."""
        self.result = """
        1 x x 1 0
        2 3 3 1 0
        1 x 1 0 0
        1 1 1 0 0
        0 0 0 0 0
        """

    def test_CommunicationStrategy1(self):
        """only com. strategy is required to solve the board."""
        self.result = """
        1 x x 1 0 0 0
        2 3 3 1 0 1 1
        1 x 1 0 0 1 x
        1 1 1 0 0 1 1
        0 1 1 1 0 0 0
        0 1 x 1 0 0 0
        0 1 1 1 0 1 1
        0 0 0 0 0 1 x
        0 0 0 0 0 1 1
        """


if __name__ == '__main__':
    unittest.main(exit=False)
