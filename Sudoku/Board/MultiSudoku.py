import time

def sudoku_solver(puzzle):
    """kata's required interface"""
    return Sudoku(problem=puzzle).solve()

class Sudoku:
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

        t1 = time.time()
        self.problem = problem
        self.valid_grid(problem)
        self.sudokuindex = list((r, c, self.blockindex(r, c)) for r in range(9) for c in range(9))
        self.solutions = []

        # TODO move to StrategySets execute (__init__)
        B = [set(self.problem[r][c] for r, c, b in self.sudokuindex
                 if self.problem[r][c] != 0 and b == i) for i in range(9)]

        self.candblock = [set(range(1, 10)) - block for block in B]
        self.candrow = [set(range(10)) - set(row) for row in self.problem]
        self.candcol = [set(range(10)) - set(column) for column in list(zip(*self.problem))]  # make use of transpose

        self.zeros = [(r, c, b) for r, c, b in self.sudokuindex if self.problem[r][c] == 0]
        if any([not bool(self.options(r, c, b)) for r, c, b in self.zeros]):
            raise ValueError('InvalidGrid: Some zero has no options.')

        self.memo = dict()
        t2 = time.time()
        print('init_time', str(t2 - t1))

    def __repr__(self):
        return '\n'.join([str(row) for row in self.solution])

    def valid_grid(self, problem):
        if len(problem) != 9 or not all([len(row) == 9 for row in problem]):
            raise ValueError('InvalidGrid: Problem is not not of proper dimensions')

        if not set.union(*[set(row) for row in problem]).issubset(set(range(10))):
            raise ValueError('InvalidGrid: Values of problem are not in range 1~9')

    @property
    def solution(self):
        """helper method to reformat dict solution to nested list format"""
        return [[self.memo[(r, c, self.blockindex(r, c))]
                 if (r, c, self.blockindex(r, c)) in self.memo.keys()
                    and self.memo[(r, c, self.blockindex(r, c))] is not None
                 else self.problem[r][c] for c in range(9)] for r in range(9)]

    @staticmethod
    def blockindex(r, c):
        return r // 3 + c // 3 + (r // 3) * 2

    def solve(self):
        # StrategyPosition.execute(self)
        pass
