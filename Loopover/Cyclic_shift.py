from Loopover.StrategyLiftshift import StrategyLiftshift
from Loopover.StrategyToprow import StrategyToprow
from Loopover.Row import Row, Node
from Loopover.Cyclic_shift_debug import Debugbehaviour


# FIXME: multiple consecutive tests fail for an unidentified reason. eventhough
#  on their own, the solution is valid

class Cyclic_shift_board(Debugbehaviour):
    direct = {'L': -1, 'R': 1, 'D': 1, 'U': -1}

    def __init__(self, mixed_up_board):
        """
        kata: https://www.codewars.com/kata/5c1d796370fee68b1e000611/train/python
        :param mixedUpBoard: two-dim arrays (or lists of lists) of symbols
        representing the initial (unsolved) grid

        Different grid sizes are tested: from 2x2 to 9x9 grids
        (including rectangular grids like 4x5)
        """

        self.mixed_up_board = mixed_up_board
        # Make the Node aware of (/allow to inquire) where the target of the currently occupying value is.
        Node.current = {val: (r, c) for r, row in enumerate(mixed_up_board) for c, val in enumerate(row)}

        # Create a playable board
        self.rows = [Row([Node((r, c), val) for c, val in enumerate(row)], r, True) for r, row in
                     enumerate(mixed_up_board)]
        self.cols = [Row(col, c, False) for c, col in enumerate(zip(*reversed(self.rows)))]
        self.rdim, self.cdim = len(self.rows[0]), len(self.cols[0])

    def __repr__(self):
        return '\n'.join([' '.join([str(val) for val in row]) for row in self.rows])

    def solve(self, solved_board):
        """Your task: return a List of moves that will transform the unsolved
           grid into the solved one. All values of the scrambled and unscrambled
           grids will be unique! Moves will be 2 character long Strings"""

        self.solved_board = solved_board
        Node.target = {val: (r, c) for r, row in enumerate(solved_board) for c, val in enumerate(row)}

        StrategyLiftshift.executeStrategy(self)

        # corner case: simple shift suffices & nothing else needs to be done
        _, t = Node.current[self.solved_board[0][0]]
        self.rows[0].shift(self.rows[0].shortest_shiftLR(t, 0))
        if self.solved_board[0] != self.rows[0].toList():
            StrategyToprow.executeStrategy(self)

        if self.solved_board != [row.toList() for row in self.rows]:  # unsolvable
            return None
        else:
            return self.solution

    @property
    def solution(self):
        return Row.Solution


if __name__ == '__main__':
    # DEBUG INTERFACE: The kata requires a loopover function
    def loopover(mixed_up_board, solved_board):
        return Cyclic_shift_board(mixed_up_board).solve(solved_board)


    # deprec: run_test & board these function was copied and adjusted from the
    #  kata's tests to emulate the behaviour. With unittests, this is obsolete
    #  and unnecessary tedious.
    def board(strboard):
        return [list(row) for row in strboard.split('\n')]

    def run_test(start, end, unsolvable):

        # print_info(board(start), board(end))
        moves = loopover(board(start), board(end))
        if unsolvable:
            assert moves is None  # 'Unsolvable configuration

        else:
            moves = tuple(moves)
            assert Cyclic_shift_board(board(start)).debug_check(moves, board(end)) == True
