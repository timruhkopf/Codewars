import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Board.Util import board


class Test_Minesweeper_behaviour(unittest.TestCase):

    def test_communication(self):
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

    def test_open_hidden_solution(self):
        # gamemap = """
        #    ? ? ? ? 0 0 0
        #    ? ? ? ? 0 ? ?
        #    ? ? ? 0 0 ? ?
        #    ? ? ? 0 0 ? ?
        #    0 ? ? ? 0 0 0
        #    0 ? ? ? 0 0 0
        #    0 ? ? ? 0 ? ?
        #    0 0 0 0 0 ? ?
        #    0 0 0 0 0 ? ?
        #    """.replace(' ', '')
        # result = """
        #    1 x x 1 0 0 0
        #    2 3 3 1 0 1 1
        #    1 x 1 0 0 1 x
        #    1 1 1 0 0 1 1
        #    0 1 1 1 0 0 0
        #    0 1 x 1 0 0 0
        #    0 1 1 1 0 1 1
        #    0 0 0 0 0 1 x
        #    0 0 0 0 0 1 1
        #    """.replace(' ', '')
        #
        # from .Solution import Solution
        #
        # # test open from context works
        # result_board = Solution(board(result))
        # m = Game(board(gamemap), n=result.count('x'), context=result_board)
        # m.open(0, 0)
        # print(m)

        pass

    def test_state_map(self):
        pass

    def test_state_recursion(self):
        """test how a position's update causes the next to update"""
        pass

    def test_state_found_bomb(self):
        """testing communicate_bombs function & found bomb"""
        pass

    def test_state_equal_qb(self):
        """the number of bombs and the number of question marks is same after state update"""
        pass

    def test_state_hitting0(self):
        """when a state update reveals the last bomb all remaining "?" neighbours
         are clear to open."""
        pass


if __name__ == '__main__':
    unittest.main(exit=False)
