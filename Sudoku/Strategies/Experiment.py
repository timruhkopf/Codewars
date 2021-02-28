from collections import deque
from copy import deepcopy
from functools import lru_cache

from Sudoku.Board.BlockView import BlockView


class Experiment:
    values = set(range(1, 10))

    def __init__(self, sudokuboard, zeros):
        self.problem = deepcopy(sudokuboard)
        self.blockview = BlockView(self.problem)
        self.columnview = lambda c: (self.problem[r][c] for r in range(len(self.problem)))

        self.unvisited = deque(zeros)  # create a copy for second run
        self.remaining_choices = dict()

    def __repr__(self):
        return '\n'.join([str(row) for row in self.problem])

    @staticmethod
    @lru_cache(maxsize=81)
    def blockindex(r, c):
        return r // 3 + c // 3 + (r // 3) * 2

    def options(self, r, c):
        """at position (r, c) in the sudoku, which are the current applicable choices"""
        b = self.blockindex(r, c)
        rs, cs, bs = set(self.problem[r]), set(self.columnview(c)), set(self.blockview[b])
        return self.values.difference(rs.union(cs, bs))

    def nextzero(self):
        """yield the next zero to choose from."""
        return self.unvisited.popleft()


if __name__ == '__main__':
    s = Experiment(sudokuboard=[[0, 9, 0, 0, 7, 1, 0, 0, 4],
                                [2, 0, 0, 0, 0, 0, 0, 7, 0],
                                [0, 0, 3, 0, 0, 0, 2, 0, 0],
                                [0, 0, 0, 9, 0, 0, 0, 3, 5],
                                [0, 0, 0, 0, 1, 0, 0, 8, 0],
                                [7, 0, 0, 0, 0, 8, 4, 0, 0],
                                [0, 0, 9, 0, 0, 6, 0, 0, 0],
                                [0, 1, 7, 8, 0, 0, 0, 0, 0],
                                [6, 0, 0, 0, 2, 0, 7, 0, 0]],
                   zeros=(0))
    assert s.options(0, 0) == {8, 5}
    assert s.options(8, 8) == {8, 1, 3, 9}

    # same block update
    s.problem[7][7] = 3
    assert s.options(8, 8) == {8, 1, 9}

    s.blockindex(3, 4)
