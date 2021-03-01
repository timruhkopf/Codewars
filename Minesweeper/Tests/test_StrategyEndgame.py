import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Strategies import Strategy_Superset, Strategy_Endgame
from ..Util import board


class TestSolvableEndgame(unittest.TestCase):

    def tearDown(self) -> None:
        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)

        while bool(m.zeros):
            zero = m.zeros.pop()
            m.open(*zero)
            placedzeros = set(n.position for n in m.clues.values() if n.clue == 0)
            m.zeros.difference_update(placedzeros)

        # (1) find sets of nodes, that are jointly informative
        Strategy_Superset.execute(m)

        Strategy_Endgame.remain_bomb_count(m)
        Strategy_Endgame.sequential_combinations(m)

        self.assertEqual(m.board, board(self.result))

        del self.result

    def test_endgame_simple(self):
        """all remaining ? after communication must be bombs due to count of bombs
         (remain_bomb_count endgame)"""

        self.result = """
        0 0 0 0 0 0 0 0 0 0 0
        0 0 0 1 2 3 3 2 1 0 0
        0 0 1 3 x x x x 1 0 0
        0 0 2 x x x x 5 2 0 0
        0 0 3 x x x x x 2 0 0
        0 0 3 x x x x x 2 0 0
        0 0 2 x x x x 3 1 0 0
        0 0 1 2 3 3 2 1 0 0 0
        0 0 0 0 0 0 0 0 0 0 0
        """

    def test_endgameStrategy(self):
        """inside the bombs are ? still - but in combination with the number of
        bombs, these positions will never be a potential bomb candidate"""
        self.result = """
        0 0 0 0 0 0 0 0 0 0 0
        0 0 0 1 2 3 3 2 1 0 0
        0 0 1 3 x x x x 1 0 0
        0 0 2 x x 6 x 5 2 0 0
        0 0 3 x 4 4 x x 2 0 0
        0 0 3 x 5 5 x x 2 0 0
        0 0 2 x x x x 3 1 0 0
        0 0 1 2 3 3 2 1 0 0 0
        0 0 0 0 0 0 0 0 0 0 0
        """

    def test_endgameStrategy2(self):
        """This test has three deterministic shapes solvable with communication
          only & one pattern on the right, that is not deterministically solvable"""

        self.result = """
        1 x 1 0 0 2 x 2 1 x 1 0 0 1 x x 1
        1 1 1 0 0 2 x 3 2 1 1 0 0 1 3 4 3
        0 0 0 0 0 1 2 x 1 0 0 0 0 0 1 x x
        0 0 0 0 0 0 1 1 1 0 0 0 0 0 1 2 2
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
        1 1 1 0 0 0 0 0 0 0 0 0 0 1 2 x 1
        1 x 1 0 0 0 0 0 0 0 0 0 0 1 x 2 1
        """

    def test_endgame4_partial(self):
        self.result = """
        0 2 x 3 1 2 1
        0 2 x 3 x 2 x
        0 2 2 3 1 3 2
        0 1 x 2 1 2 x
        0 1 2 3 x 2 1
        0 0 1 x 2 1 0
        """
        # after open zeros
        """
        0 2 x ? ? ? ?
        0 2 x 3 ? ? ? 
        0 2 2 3 ? ? ?
        0 1 x 2 ? ? ?
        0 1 2 ? ? 2 1
        0 0 1 ? ? 1 0
        """

    def test_endgame4(self):
        """test endgame for more than 3 remaining bombs"""
        self.result = """
        0 0 0 1 x 1 1 x 1 0 0 0 0 0 1 1 1 0 0 1 x 3 x 3 1 2 1
        1 1 0 1 1 1 1 1 1 0 0 0 0 0 1 x 1 1 1 2 1 3 x 3 x 2 x
        x 2 1 1 0 0 0 0 0 0 1 1 1 0 1 1 1 1 x 1 0 2 2 3 1 3 2
        1 2 x 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 1 x 2 1 2 x
        0 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 1 2 3 x 2 1
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
        """
    # TODO check if it works, when the n
    #  if bool(self.remain_bomb) and self.remain_bomb <= 3:
    #  self.remain_bomb <= 3 condition is changed to more bombs!

    # def test_random_boards(self):
    #     pass

    # TODO: add simplified superset & endgame test cases to showcase the idea!
    #  do this after refactoring superset in multiple subfunctions


if __name__ == '__main__':
    unittest.main(exit=False)
