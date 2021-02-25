import time


def sudoku_solver(puzzle):
    return Sudoku(problem=puzzle).solve()


# TODO: make a check functino, that cares only for the current state
#  abandon sets - their updates take tooo damn long for multiple sudoku. Test cases
#  work locally though

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

        t1 = time.time()
        self.problem = problem
        self.valid_grid(problem)
        self.sudokuindex = list((r, c, self.blockindex(r, c)) for r in range(9) for c in range(9))

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

    def options(self, r, c, b, reverse=False):
        """returns sorted intersection of possible values at that location"""
        intersect = self.candrow[r] & self.candcol[c] & self.candblock[b]
        return sorted(intersect, reverse=reverse)

    def _solve_single(self, position, current_idx, reverse=False):
        '''
        recursive path trough the problem,
        whilst considering only applicable paths.
        :returns Single solution, that is the result of traversing on sorted
        options
        '''
        r, c, b = position
        for s in self.options(*position, reverse):
            if current_idx + 1 == len(self.zeros):  # base case: last zero value is reached
                self.memo[position] = s
                return s
            else:  # go further down on path with current s
                self.memo[position] = s  # DEPREC: REMOVE ME this is only for debug
                self.candrow[r].difference_update({s})
                self.candcol[c].difference_update({s})
                self.candblock[b].difference_update({s})
                sol = self._solve_single(
                    self.zeros[current_idx + 1], current_idx + 1, reverse)

                if bool(sol):  # the next step returned a non empty solution
                    self.memo[position] = s
                    return s

                else:  # the next zero index returns None
                    # i.e. it has no applicable choices: Go up
                    # add s to sets it was removed from
                    self.candrow[r].update({s})
                    self.candcol[c].update({s})
                    self.candblock[b].update({s})
                    if position in self.memo.keys():
                        self.memo.pop(position)
                    continue
        return None

    def solve(self):
        t1 = time.time()
        self._solve_single(position=self.zeros[0], current_idx=0, reverse=False)
        t2 = time.time()
        print('solve_single 1st ', str(t2 - t1))

        solution = self.solution
        if solution == self.problem:
            raise ValueError('InvalidSolution: Unsolvable Sudoku')

        second = Sudoku(self.problem)
        t1 = time.time()
        second._solve_single(self.zeros[0], current_idx=0, reverse=True)

        t2 = time.time()
        print('solve_single 2nd ', str(t2 - t1))
        print('')

        if solution != second.solution:
            raise ValueError('InvalidSolution: Sudoku has multiple Solutions')

        return self.solution


