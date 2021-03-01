from copy import deepcopy
from functools import lru_cache
from itertools import chain

from Sudoku.Strategies.StrategyForward import StrategyForward, StrategyAll
from Sudoku.Strategies.Strategyforwardbackward import Strategyforwardbackward


class Sudoku:
    values = set(range(1, 10))
    blockrefs = list(chain(*[[(rref, cref) for cref in (0, 3, 6)] for rref in (0, 3, 6)]))

    def __init__(self, sudokuboard):
        self.problem = sudokuboard
        self.zeros = [(r, c) for r, row in enumerate(self.problem) for c, v in enumerate(row) if v == 0]
        self.valid_grid_basic()

        self.solutions = []

    def __repr__(self):
        """printing the current state of the solver"""
        return '\n'.join([str(row) for row in self.problem])

    def blockview(self, b):
        """
        :param b: blockindex (by convention: rowwise)
        :returns: generator object, iterating a 'rowlike' version of the block"""
        rref, cref = self.blockrefs[b]
        return chain(*(self.problem[rref + i][cref:cref + 3] for i in range(3)))

    def columnview(self, c):
        """
        :param c: columnindex
        :returns: generator object, iterating a 'rowlike' version of the column"""
        return (self.problem[r][c] for r in range(len(self.problem)))

    @staticmethod
    @lru_cache(maxsize=81)
    def blockindex(r, c):
        return r // 3 + c // 3 + (r // 3) * 2

    def options(self, r, c):
        """at position (r, c) in the sudoku, which are the current applicable choices"""
        b = self.blockindex(r, c)
        rs, cs, bs = set(self.problem[r]), set(self.columnview(c)), set(self.blockview(b))
        return self.values.difference(rs.union(cs, bs))

    def valid_grid_basic(self):
        """check at initialisation if board is shaped and filled like a sudoku board
        checks if at init, the board is playable (unique values & each position has choices)"""
        if len(self.problem) != 9 or not all([len(row) == 9 for row in self.problem]):
            raise ValueError('InvalidGrid: problem is not not of proper dimensions')

        # check if any character is invalid
        if not set.union(*[set(row) for row in self.problem]).issubset(set(range(10))):
            raise ValueError('InvalidGrid: Values of problem are not in range 1~9')

        counts = ([row.count(x) for x in range(1, 10) if x in row]
                  for view in (self.problem, zip(*self.problem),
                               (list(self.blockview(index)) for index in range(9)))
                  for row in view)
        if any([len(c) != sum(c) for c in counts]):
            raise ValueError('Detected multiple same values in row, column or block')

        if not all((len(self.options(*zero)) > 0 for zero in self.zeros)):
            raise ValueError('Some positions do not have any options at the beginning')

    def solve(self, strategy='f'):
        """Kata's required solver"""
        if strategy == 'fb':  # TODO add multiple Strategies
            Strategyforwardbackward.execute(self)
        elif strategy == 'f':
            StrategyForward.execute(self)
        elif strategy == 'all':
            StrategyAll.execute(self)

        return self.solutions[0]

    def append_solution(self):
        # check recursion found a solution. solutions are guaranteed to be valid.
        if not any([row.count(0) for row in self.problem]):
            self.solutions.append(deepcopy(self.problem))
            return True
        else:
            return False


if __name__ == '__main__':
    problem = [[0, 9, 0, 0, 7, 1, 0, 0, 4],
               [2, 0, 0, 0, 0, 0, 0, 7, 0],
               [0, 0, 3, 0, 0, 0, 2, 0, 0],
               [0, 0, 0, 9, 0, 0, 0, 3, 5],
               [0, 0, 0, 0, 1, 0, 0, 8, 0],
               [7, 0, 0, 0, 0, 8, 4, 0, 0],
               [0, 0, 9, 0, 0, 6, 0, 0, 0],
               [0, 1, 7, 8, 0, 0, 0, 0, 0],
               [6, 0, 0, 0, 2, 0, 7, 0, 0]]
    solution = [[5, 9, 8, 2, 7, 1, 3, 6, 4],
                [2, 4, 6, 3, 8, 5, 9, 7, 1],
                [1, 7, 3, 4, 6, 9, 2, 5, 8],
                [8, 6, 2, 9, 4, 7, 1, 3, 5],
                [9, 3, 4, 5, 1, 2, 6, 8, 7],
                [7, 5, 1, 6, 3, 8, 4, 9, 2],
                [4, 2, 9, 7, 5, 6, 8, 1, 3],
                [3, 1, 7, 8, 9, 4, 5, 2, 6],
                [6, 8, 5, 1, 2, 3, 7, 4, 9]]
    s = Sudoku(problem)

    assert s.solve() == solution

    s = Experiment(sudokuboard=[[0, 9, 0, 0, 7, 1, 0, 0, 4],
                                [2, 0, 0, 0, 0, 0, 0, 7, 0],
                                [0, 0, 3, 0, 0, 0, 2, 0, 0],
                                [0, 0, 0, 9, 0, 0, 0, 3, 5],
                                [0, 0, 0, 0, 1, 0, 0, 8, 0],
                                [7, 0, 0, 0, 0, 8, 4, 0, 0],
                                [0, 0, 9, 0, 0, 6, 0, 0, 0],
                                [0, 1, 7, 8, 0, 0, 0, 0, 0],
                                [6, 0, 0, 0, 2, 0, 7, 0, 0]],
                   )

    # TODO write test casess for options & blockindex
    assert s.options(0, 0) == {8, 5}
    assert s.options(8, 8) == {8, 1, 3, 9}

    # same block update
    s.problem[7][7] = 3
    assert s.options(8, 8) == {8, 1, 9}

    s.blockindex(3, 4)

    # TODO write TESTCASES:
    # aproblem = [[v + i for v in range(9)] for i in range(0, 81, 9)]
    # assert list(blockView(0)) == [0, 1, 2, 9, 10, 11, 18, 19, 20]
    # assert list(blockView(1)) == [3, 4, 5, 12, 13, 14, 21, 22, 23]
    # assert list(blockView(4)) == [30, 31, 32, 39, 40, 41, 48, 49, 50]
    # assert list(blockView(8)) == [60, 61, 62, 69, 70, 71, 78, 79, 80]
