import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Util import board


class TestMinesweeperSolvables(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)
        m.solve()

        self.assertEqual(m.board, board(self.result))

        del self.result

    def test_CommunicationPartial1(self):
        self.result = """
        1 x 1 0
        1 1 1 0
        0 0 0 0
        """

    def test_CommunicationPartial2(self):
        self.result = """
        0 2 x 2 1 x 1 0
        0 2 x 3 2 1 1 0
        0 1 2 x 1 0 0 0
        0 0 1 1 1 0 0 0
        0 0 0 0 0 0 0 0
        """

    def test_CommunicationStrategy0(self):
        """partial of Com.Strategy 1: only com. strategy is required to solve the board."""
        self.result = """
        0 0 0
        0 1 1
        0 1 x
        0 1 1
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
