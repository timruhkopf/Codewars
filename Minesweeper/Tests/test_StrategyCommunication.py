import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Board.Util import board


class Test_Strategy_Communication(unittest.TestCase):

    def test_CommunicationStrategy(self):
        """only com. strategy is required to solve the board."""
        result = """
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

        solution = Solution(board(result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)
        self.assertEqual(m.solve(), board(result))


if __name__ == '__main__':
    unittest.main(exit=False)
