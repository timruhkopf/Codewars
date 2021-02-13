import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Util import board


class TestMinesweeperProblems(unittest.TestCase):
    def test_CommunicationStrategy0(self):
        """only com. strategy is required to solve the board."""
        result = """
            0 0 0
            0 1 1
            0 1 x
            0 1 1
        """

        solution = Solution(board(result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)
        m.solve()

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
        m = Game(board=solution.covered_board, n=solution.n, context=solution)
        m.solve()

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
        m = Game(board=solution.covered_board, n=solution.n, context=solution)
        m.solve()

        self.assertEqual(m.board, board(result))

    # def test_endgameStrategy(self):
    #     result = """
    #     0 0 0 0 0 0 0 0 0 0 0
    #     0 0 0 1 2 3 3 2 1 0 0
    #     0 0 1 3 x x x x 1 0 0
    #     0 0 2 x x 6 x 5 2 0 0
    #     0 0 3 x 4 4 x x 2 0 0
    #     0 0 3 x 5 5 x x 2 0 0
    #     0 0 2 x x x x 3 1 0 0
    #     0 0 1 2 3 3 2 1 0 0 0
    #     0 0 0 0 0 0 0 0 0 0 0
    #     """
    #     solution = Solution(board(result))
    #     m = Game(board=solution.covered_board, n=solution.n, context=solution)
    #     self.assertEqual(m.solve(), board(result))
    #
    # def test_endgameStrategy2(self):
    #     result = """
    #     1 x 1 0 0 2 x 2 1 x 1 0 0 1 x x 1
    #     1 1 1 0 0 2 x 3 2 1 1 0 0 1 3 4 3
    #     0 0 0 0 0 1 2 x 1 0 0 0 0 0 1 x x
    #     0 0 0 0 0 0 1 1 1 0 0 0 0 0 1 2 2
    #     0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
    #     1 1 1 0 0 0 0 0 0 0 0 0 0 1 2 x 1
    #     1 x 1 0 0 0 0 0 0 0 0 0 0 1 x 2 1
    #     """
    #     solution = Solution(board(result))
    #     m = Game(board=solution.covered_board, n=solution.n, context=solution)
    #     self.assertEqual(m.solve(), board(result))
    #
    # def test_endgame3(self):
    #     result = """
    #     0 0 0 0 0 0 0 0 0 0 0
    #     0 0 0 1 2 3 3 2 1 0 0
    #     0 0 1 3 x x x x 1 0 0
    #     0 0 2 x x x x 5 2 0 0
    #     0 0 3 x x x x x 2 0 0
    #     0 0 3 x x x x x 2 0 0
    #     0 0 2 x x x x 3 1 0 0
    #     0 0 1 2 3 3 2 1 0 0 0
    #     0 0 0 0 0 0 0 0 0 0 0
    #     """
    #     solution = Solution(board(result))
    #     m = Game(board=solution.covered_board, n=solution.n, context=solution)
    #     self.assertEqual(m.solve(), board(result))
    #     pass
    #
    # def test_endgame4(self):
    #     result = """
    #     0 0 0 1 x 1 1 x 1 0 0 0 0 0 1 1 1 0 0 1 x 3 x 3 1 2 1
    #     1 1 0 1 1 1 1 1 1 0 0 0 0 0 1 x 1 1 1 2 1 3 x 3 x 2 x
    #     x 2 1 1 0 0 0 0 0 0 1 1 1 0 1 1 1 1 x 1 0 2 2 3 1 3 2
    #     1 2 x 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 1 x 2 1 2 x
    #     0 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 1 2 3 x 2 1
    #     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
    #     """
    #     # TODO check if it works, when the n
    #     #  if bool(self.remain_bomb) and self.remain_bomb <= 3:
    #     #  self.remain_bomb <= 3 condition is changed to more bombs!
    #     solution = Solution(board(result))
    #     m = Game(board=solution.covered_board, n=solution.n, context=solution)
    #     self.assertEqual(m.solve(), board(result))

    def test_unsolvable1(self):
        # # Ambivalent state
        #     gamemap = """
        #     0 ? ?
        #     0 ? ?
        #     """.strip()
        #     result = """
        #     0 1 x
        #     0 1 1
        #     """.strip()
        #     assert solve_mine(gamemap, result.count('x'), result) == "?"
        pass

    def test_unsolvable2(self):
        """Huge ambivalent state"""

        #     result = """
        #     1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
        #     x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
        #     1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
        #     0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
        #     0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
        #     0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
        #     0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
        #     0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
        #     0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
        #     0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
        #     0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
        #     0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
        #     0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
        #     0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
        #     0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
        #     0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
        #     0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
        #     0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
        #     0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
        #     0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
        #     0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
        #     0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
        #     0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
        #     """.strip()
        #     assert solve_mine(gamemap, result.count('x'), result) == "?"
        pass

    def test_unsolvable3(self):
        # # differently shaped ambivalent state
        #     gamemap = """
        #     0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? 0 ? ? ?
        #     0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ?
        #     0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ?
        #     0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? ? ? ? 0
        #     ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ?
        #     ? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ?
        #     ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ?
        #     ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
        #     ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
        #     """.strip()
        #     result = """
        #     0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
        #     0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
        #     0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
        #     0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
        #     1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
        #     x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
        #     2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
        #     1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
        #     1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
        #     """.strip()
        #     assert solve_mine(gamemap, result.count('x'), result) == "?"
        pass

    def test_random_boards(self):
        pass

    # TODO: add simplified superset & endgame test cases to showcase the idea!
    #  do this after refactoring superset in multiple subfunctions


if __name__ == '__main__':
    unittest.main(exit=False)
