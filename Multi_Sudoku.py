from functools import wraps
from copy import deepcopy

def memoize(f):
    """decorator to memoize the results of the recursive call"""

    @wraps(f)
    def helper(self, position, *args, **kwargs):
        helper.calls += 1
        helper.memo[position] = f(self, position, *args, **kwargs)
        return helper.memo[position]

    helper.calls = 0
    helper.memo = {}
    return helper


class Sudoku:
    def __init__(self, problem):
        """
        https://www.codewars.com/kata/5588bd9f28dbb06f43000085
        TASK:
        Write a function that solves sudoku puzzles of any difficulty.
        The function will take a sudoku grid and it should return a 9x9
        array with the proper answer for the puzzle.

        :raises
        (0) invalid grid (not 9x9, cell with values not in the range 1~9);
        (1) multiple solutions for the same puzzle
        (2) the puzzle is unsolvable
        """

        self.problem = problem

        self.sudokuindex = list((r, c, self.blockindex(r, c)) for r in range(9) for c in range(9))

        B = [set(self.problem[r][c] for r, c, b in self.sudokuindex
                 if self.problem[r][c] != 0 and b == i) for i in range(9)]

        self.candblock = [set(range(1, 10)) - block for block in B]
        self.candrow = [set(range(10)) - set(row) for row in self.problem]
        self.candcol = [set(range(10)) - set(column) for column in list(zip(*self.problem))]  # make use of transpose

        self.valid_grid(problem)
        self.zero = [(r, c, b) for r, c, b in self.sudokuindex if self.problem[r][c] == 0]
        if any([not bool(self.options(r, c, b)) for r, c, b in self.zero]):
            raise ValueError('This Grid is invalid. Some zero has no options.')

        self.memo = dict()

    def __repr__(self):
        return '\n'.join([str(row) for row in self.solution])

    @staticmethod
    def blockindex(r, c):
        return r // 3 + c // 3 + (r // 3) * 2

    @property
    def solution(self):
        """helper method to reformat dict solution to nested list format"""
        return [[self.memo[(r, c, self.blockindex(r, c))]
                 if (r, c, self.blockindex(r, c)) in self.memo.keys()
                    and self.memo[(r, c, self.blockindex(r, c))] is not None
                 else self.problem[r][c] for c in range(9)] for r in range(9)]

    def options(self, r, c, b, reverse=False):
        """returns sorted intersection of possible values at that location"""
        intersect = self.candrow[r] & self.candcol[c] & self.candblock[b]
        return sorted(intersect, reverse=reverse)

    @memoize
    def _solve_single(self, position, counter, reverse=False):
        '''
        recursive path trough the problem,
        whilst considering only applicable paths.
        :returns Single solution, that is the result of traversing on sorted
        options
        '''
        r, c, b = position
        for s in self.options(*position, reverse):  # TODO : by a boolean argument option must be reversible
            if counter + 1 == len(self.zero):  # base case: last zero value is reached
                return s
            else:  # go further down on path with current s
                self.candrow[r].difference_update({s})
                self.candcol[c].difference_update({s})
                self.candblock[b].difference_update({s})
                sol = self._solve_single(
                    self.zero[counter + 1], counter + 1, reverse)

                if bool(sol):  # the next step returned a non empty solution
                    return s

                else:  # the next zero index returns None
                    # i.e. it has no applicable choices: Go up
                    # add s to sets it was removed from
                    self.candrow[r].update({s})
                    self.candcol[c].update({s})
                    self.candblock[b].update({s})
                    continue
        return None

    def solve(self):
        """
        first solve_single with sorted options
        for check on second solution:
        fill the sudoku until zeros position [:-1] and try to solve
        with reversed options. if unsuccessful fill until zeros_position [:-2]
        continue until we reach the very exact solution as before (i.e.
        there is only this solution) EARLY STOP - once the first differing
        solution is found, throw an error!
        """
        self._solve_single(position=self.zero[0], counter=0, reverse=False)
        self.memo = deepcopy(self._solve_single.memo)

        if self.solution == self.problem:
            raise ValueError('This Sudoku has no solutions')

        for i in range(2, len(self.zero) + 1):
            unfinished = deepcopy(self.problem)
            for (r, c, b) in self.zero[:-i]:
                val = self.memo[(r, c, b)]
                if val is not None:
                    unfinished[r][c] = val
            uSudoku = Sudoku(unfinished)
            uSudoku._solve_single(position=self.zero[-i], counter=0, reverse=True)
            uSudoku.memo = uSudoku._solve_single.memo

            if uSudoku.solution != unfinished and \
                    uSudoku.solution != self.solution:
                for row, row1 in zip(self.solution, uSudoku.solution):
                    print(row, '\n', row1)
                raise ValueError('This Sudoku has multiple solutions')

        return self.solution

    def valid_grid(self, problem):
        if len(problem) != 9 or not all([len(row) == 9 for row in problem]):
            raise ValueError('Problem is not not of proper dimensions')

        if set.union(*[set(row) for row in problem]) != set(range(10)):
            raise ValueError('Values of problem are not in range 1~9')

    def valid_solution(self):
        """for debugging only"""
        s = set(range(1, 10))
        solved = self.solution

        if not all([self.solution[r][c] == self.problem[r][c]
                    for r, c, b in self.sudokuindex if self.problem[r][c] != 0]):
            raise ValueError('You are not allowed to alter the nonzero values of problem')

        B = [set(solved[r][c] for r, c, b in self.sudokuindex if b == i) for i in range(9)]

        blocksets = all([block == s for block in B])
        rowsets = all([set(row) == s for row in solved])
        colsets = all([set(col) == s for col in zip(*solved)])

        if not (rowsets and colsets and blocksets):
            raise ValueError('Solution is invalid')


def sudoku_solver(puzzle):
    # Codewars expected interface
    s = Sudoku(problem=puzzle)
    return s.solve()


if __name__ == '__main__':
    # deterministic case, test case of codewars:
    problem = [[0, 0, 6, 1, 0, 0, 0, 0, 8],
               [0, 8, 0, 0, 9, 0, 0, 3, 0],
               [2, 0, 0, 0, 0, 5, 4, 0, 0],
               [4, 0, 0, 0, 0, 1, 8, 0, 0],
               [0, 3, 0, 0, 7, 0, 0, 4, 0],
               [0, 0, 7, 9, 0, 0, 0, 0, 3],
               [0, 0, 8, 4, 0, 0, 0, 0, 6],
               [0, 2, 0, 0, 5, 0, 0, 8, 0],
               [1, 0, 0, 0, 0, 2, 5, 0, 0]]

    solution = [[3, 4, 6, 1, 2, 7, 9, 5, 8],
                [7, 8, 5, 6, 9, 4, 1, 3, 2],
                [2, 1, 9, 3, 8, 5, 4, 6, 7],
                [4, 6, 2, 5, 3, 1, 8, 7, 9],
                [9, 3, 1, 2, 7, 8, 6, 4, 5],
                [8, 5, 7, 9, 4, 6, 2, 1, 3],
                [5, 9, 8, 4, 1, 3, 7, 2, 6],
                [6, 2, 4, 7, 5, 9, 3, 8, 1],
                [1, 7, 3, 8, 6, 2, 5, 9, 4]]

    p = Sudoku(problem)
    p.solve()
    p.valid_solution()
    assert p.solution == solution

    # deterministic case
    problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],
               [0, 0, 0, 4, 0, 6, 0, 0, 0],
               [0, 0, 5, 0, 7, 0, 3, 0, 0],
               [0, 6, 0, 0, 0, 0, 0, 4, 0],
               [4, 0, 1, 0, 6, 0, 5, 0, 8],
               [0, 9, 0, 0, 0, 0, 0, 2, 0],
               [0, 0, 7, 0, 3, 0, 2, 0, 0],
               [0, 0, 0, 7, 0, 5, 0, 0, 0],
               [1, 0, 0, 0, 4, 0, 0, 0, 7]]

    solution = [[9, 2, 6, 5, 8, 3, 4, 7, 1],
                [7, 1, 3, 4, 2, 6, 9, 8, 5],
                [8, 4, 5, 9, 7, 1, 3, 6, 2],
                [3, 6, 2, 8, 5, 7, 1, 4, 9],
                [4, 7, 1, 2, 6, 9, 5, 3, 8],
                [5, 9, 8, 3, 1, 4, 7, 2, 6],
                [6, 5, 7, 1, 3, 8, 2, 9, 4],
                [2, 8, 4, 7, 9, 5, 6, 1, 3],
                [1, 3, 9, 6, 4, 2, 8, 5, 7]]

    p = Sudoku(problem)
    p.solve()
    p.valid_solution()
    assert p.solution == solution
    # FIXME: somehow, the state is kept between instances of solving:
    #  if the first problem is executed in advance, this assert fails!
    #  look at last position: the 7 is replaced by the last problem's solution value 4

    # # invalid dimensions:
    problem = [[1, 1, 3, 4, 5, 6, 7, 8, 9],
               [4, 0, 6, 7, 8, 9, 1, 2, 3],
               [7, 8, 9, 1, 2, 3, 4, 5, 6],
               [2, 3, 4, 5, 6, 7, 8, 9],
               [5, 6, 7, 8, 9, 1, 2, 3, 4],
               [8, 9, 1, 2, 3, 4, 5, 6, 7],
               [3, 4, 5, 6, 7, 8, 9, 1, 2],
               [6, 7, 8, 9, 1, 2, 3, 4, 5],
               [9, 1, 2, 3, 4, 5, 6, 7, 8]]

    p = Sudoku(problem)

    # unsolvable ones:
    problem = [[0, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 5, 6, 7, 8, 9, 0, 2, 3],
               [7, 8, 9, 1, 2, 3, 4, 5, 6],
               [2, 3, 4, 5, 6, 7, 8, 9, 1],
               [5, 6, 7, 8, 9, 1, 2, 3, 4],
               [8, 9, 1, 2, 3, 4, 5, 6, 7],
               [3, 4, 5, 6, 7, 8, 9, 1, 2],
               [6, 7, 8, 9, 1, 2, 3, 4, 5],
               [9, 1, 2, 3, 4, 5, 6, 7, 8]]

    p = Sudoku(problem)
