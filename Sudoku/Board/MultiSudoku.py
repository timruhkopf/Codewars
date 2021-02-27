from functools import lru_cache

from Sudoku.Board.BlockView import BlockView, ColumnView


def sudoku_solver(puzzle):
    """kata's required interface"""
    return Sudoku(problem=puzzle).solve()


class Sudoku:
    values = set(range(1, 10))

    def __init__(self, problem):
        """
        https://www.codewars.com/kata/5588bd9f28dbb06f43000085
        TASK:
        Write a function that solves sudoku puzzles of any difficulty.
        The function will take a sudoku grid and it should return a 9x9
        array with the proper answer for the puzzle.
        :param problem: list of lists
        :raises
        (0) invalid grid (not 9x9, cell with values not in the range 1~9);
        (1) multiple solutions for the same puzzle
        (2) the puzzle is unsolvable
        """
        self.problem = problem
        self.blockview = BlockView(self.problem)
        self.columnview = ColumnView(self.problem)

        self.valid_grid()
        self.solutions = []

        # self.sudokuindex = list((r, c, self.blockindex(r, c)) for r in range(9) for c in range(9))

    def __repr__(self):
        return '\n'.join([str(row) for row in self.solution])

    def valid_grid(self):
        if len(self.problem) != 9 or not all([len(row) == 9 for row in self.problem]):
            raise ValueError('InvalidGrid: Problem is not not of proper dimensions')

        # check any character is invalid
        if not set.union(*[set(row) for row in self.problem]).issubset(set(range(10))):
            raise ValueError('InvalidGrid: Values of problem are not in range 1~9')

        # # deprec check doubles:
        # # generate block iterable (blocks represented as rows
        # blockindex = sorted([(r, c, self.blockindex(r, c)) for r in range(9) for c in range(9)], key=lambda x: x[2])
        # blocks = (blockindex[i:i + 9] for i in range(0, 81, 9))
        # blocks = ([self.problem[r][c] for r, c, b in block] for block in blocks)

        counts = ([row.count(x) for x in range(1, 10) if x in row]
                  for problem in (self.problem, zip(*self.problem), self.blockview)
                  for row in problem)
        if any([len(c) != sum(c) for c in counts]):
            raise ValueError('Detected multiple same values in row, column or block')

    def options(self, r, c):
        b = self.blockindex(r, c)
        rs, cs, bs = set(self.problem[r]), set(self.columnview[c]), set(self.blockview[b])
        return self.values.difference(rs.union(cs, bs))

    @property
    def solution(self):
        """helper method to reformat dict solution to nested list format"""
        return [[self.memo[(r, c, self.blockindex(r, c))]
                 if (r, c, self.blockindex(r, c)) in self.memo.keys()
                    and self.memo[(r, c, self.blockindex(r, c))] is not None
                 else self.problem[r][c] for c in range(9)] for r in range(9)]

    @staticmethod
    @lru_cache(maxsize=81)
    def blockindex(r, c):
        return r // 3 + c // 3 + (r // 3) * 2


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

    s.options(0, 0)
    s.blockindex(3, 4)

    assert s.solve() == solution
