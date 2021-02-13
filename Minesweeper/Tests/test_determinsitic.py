import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Board.Solver import Solver
from ..Strategies.StrategyCommunication import StrategyOpenZero
from ..Util import board


# TODO make more explicit which strategy is tested, by creating a board that is solved
#  up until it must be solved using this strategy!
#  make the following examples complete problems only - i.e. rename them.
#  (make descendants of them, that are partially solved and use explicit strategies
#  to progress in seperate test cases.

class TestCommunication(unittest.TestCase):
    def test_CommunicationStrategy0(self):
        """only com. strategy is required to solve the board."""
        result = """
            0 0 0
            0 1 1
            0 1 x
            0 1 1
        """

        solution = Solution(board(result))
        for i in range(10):
            m = Game(board=solution.covered_board, n=solution.n, context=solution)
            StrategyOpenZero.execute(m)
            self.assertEqual(m.board, board(result))

    def test_CommunicationStrategy01(self):
        """only com. strategy is required to solve the board."""
        result = """
        1 x x 1 0
        2 3 3 1 0
        1 x 1 0 0
        1 1 1 0 0 
        0 0 0 0 0
        """

        solution = Solution(board(result))
        for i in range(10):
            m = Game(board=solution.covered_board, n=solution.n, context=solution)
            StrategyOpenZero.execute(m)
            self.assertEqual(m.board, board(result))

    def test_CommunicationStrategy1(self):
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
        for i in range(10):
            # m = Game(board=solution.covered_board, n=solution.n, context=solution)
            m = Solver(board=solution.covered_board, n=solution.n, context=solution)
            m.solve()
            self.assertEqual(m.board, board(result))
