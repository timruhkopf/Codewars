import unittest

from ..Board.Game import Game
from ..Board.Solution import Solution
from ..Util import board


class Test_Minesweeper_behaviour(unittest.TestCase):

    def test_zero_removal(self):
        """this example is intended to display that only one zero per group must
        be opened- as all others zeros and neighbouring integers are opened by recursion"""
        self.result = """
        0 0 1 0
        0 0 1 0
        """

        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)

        # opening a single zero suffices to recursively communicate ('open') all zeros
        # & remove them from m.zeros entirely
        count = 0
        while bool(m.zeros):
            zero = m.zeros.pop()
            m.open(*zero)

            placedzeros = set(n.position for n in m.clues.values() if n.clue == 0)
            m.zeros.difference_update(placedzeros)
            count += 1

        self.assertEqual(count, 2)
        self.assertEqual(m.board, board(self.result))
        self.assertEqual(m.zeros, set())

    def test_intermediate_communication0(self):
        """the bomb is found by intermediate (recursive) communication.
        0 opens 1, 1 checks state == no.'?' and determines it found a bomb"""
        self.result = """
        x 1 0
        """

        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)

        # opening a single zero suffices to recursively communicate ('open') all zeros
        # & remove them from m.zeros entirely
        zero = m.zeros.pop()
        m.open(*zero)

        self.assertEqual(m.board, board(self.result))

    def test_intermediate_communication1(self):
        """single open of neighbours does not suffice,
        first zero opens all its neighb. and the neighb"""

        self.result = """
        x 2 0
        x 2 0
        """

        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)

        # opening a single zero suffices to recursively communicate ('open') all zeros
        # & remove them from m.zeros entirely
        zero = m.zeros.pop()
        m.open(*zero)

        placedzeros = set(n.position for n in m.clues.values() if n.clue == 0)
        m.zeros.difference_update(placedzeros)

        self.assertEqual(m.zeros, set())
        self.assertEqual(m.board, board(self.result))

    def test_intermediate_communication2(self):
        """multiple calls upon same position (1,2) that check its state and ?
        conditions are required  to find the bomb.
        + afterwards, the 1 in the corner is found by
        the bomb reducing state of its neighbours to 0 -- > and either (1,0)
        or (1,1) invoke open all remaining questionmarks"""

        self.result = """
           1 x 1 0
           1 1 1 0
           0 0 0 0
           """

        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)

        # opening a single zero suffices to recursively communicate ('open') all zeros
        # & remove them from m.zeros entirely
        zero = (0, 3)
        m.open(*zero)

        placedzeros = set(n.position for n in m.clues.values() if n.clue == 0)
        m.zeros.difference_update(placedzeros)

        self.assertEqual(m.zeros, set())
        self.assertEqual(m.board, board(self.result))

    def test_intermediate_communication3(self):
        """single open of neighbours does not suffice"""

        self.result = """
        0 1 x 1 0
        1 2 1 1 0
        x 1 0 0 0
        1 1 0 0 0
        0 0 0 0 0
        """

        solution = Solution(board(self.result))
        m = Game(board=solution.covered_board, n=solution.n, context=solution)

        # opening a single zero suffices to recursively communicate ('open') all zeros
        # & remove them from m.zeros entirely

        while bool(m.zeros):
            zero = m.zeros.pop()
            m.open(*zero)

            placedzeros = set(n.position for n in m.clues.values() if n.clue == 0)
            m.zeros.difference_update(placedzeros)

        self.assertEqual(m.board, board(self.result))


if __name__ == '__main__':
    unittest.main(exit=False)
