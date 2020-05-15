import time


def sudoku_solver(puzzle):
    return Sudoku(problem=puzzle).solve()


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


if __name__ == '__main__':
    # (BRUTAL) -----------------------------------------------------------------
    #  fixme killing my time
    problem = [[0, 0, 0, 0, 0, 2, 7, 5, 0],
               [0, 1, 8, 0, 9, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [4, 9, 0, 0, 0, 0, 0, 0, 0],
               [0, 3, 0, 0, 0, 0, 0, 0, 8],
               [0, 0, 0, 7, 0, 0, 2, 0, 0],
               [0, 0, 0, 0, 3, 0, 0, 0, 9],
               [7, 0, 0, 0, 0, 0, 0, 0, 0],
               [5, 0, 0, 0, 0, 0, 0, 8, 0]]
    solution = [[9, 4, 6, 1, 8, 2, 7, 5, 3],
                [3, 1, 8, 5, 9, 7, 4, 2, 6],
                [2, 7, 5, 6, 4, 3, 8, 9, 1],
                [4, 9, 2, 3, 1, 8, 5, 6, 7],
                [6, 3, 7, 2, 5, 4, 9, 1, 8],
                [8, 5, 1, 7, 6, 9, 2, 3, 4],
                [1, 2, 4, 8, 3, 5, 6, 7, 9],
                [7, 8, 3, 9, 2, 6, 1, 4, 5],
                [5, 6, 9, 4, 7, 1, 3, 8, 2]]
    assert Sudoku(problem).solve() == solution

    # randomtest:  Fixme killing my time
    problem = [[0, 5, 7, 2, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 9, 0, 8, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 9, 4],
               [8, 0, 0, 0, 0, 0, 0, 3, 0],
               [0, 0, 2, 0, 0, 7, 0, 0, 0],
               [9, 0, 0, 0, 3, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 7],
               [0, 8, 0, 0, 0, 0, 0, 0, 5]]

    Sudoku(problem).solve()

    problem = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 3, 6, 0, 0, 0, 0, 0],
               [0, 7, 0, 0, 9, 0, 2, 0, 0],
               [0, 5, 0, 0, 0, 7, 0, 0, 0],
               [0, 0, 0, 0, 4, 5, 7, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 3, 0],
               [0, 0, 1, 0, 0, 0, 0, 6, 8],
               [0, 0, 8, 5, 0, 0, 0, 1, 0],
               [0, 9, 0, 0, 0, 0, 4, 0, 0]]

    solution = [[8, 1, 2, 7, 5, 3, 6, 4, 9],
                [9, 4, 3, 6, 8, 2, 1, 7, 5],
                [6, 7, 5, 4, 9, 1, 2, 8, 3],
                [1, 5, 4, 2, 3, 7, 8, 9, 6],
                [3, 6, 9, 8, 4, 5, 7, 2, 1],
                [2, 8, 7, 1, 6, 9, 5, 3, 4],
                [5, 2, 1, 9, 7, 4, 3, 6, 8],
                [4, 3, 8, 5, 2, 6, 9, 1, 7],
                [7, 9, 6, 3, 1, 8, 4, 5, 2]]
    assert Sudoku(problem).solve() == solution  # FIXME: backword path is slow: ~6.88 s

    # (single solutions) -------------------------------------------------------
    problem = [[0, 9, 6, 5, 0, 4, 0, 7, 1],
               [0, 2, 0, 1, 0, 0, 0, 0, 0],
               [0, 1, 4, 0, 9, 0, 6, 2, 3],
               [0, 0, 3, 0, 6, 0, 0, 8, 0],
               [0, 0, 8, 0, 5, 0, 4, 0, 0],
               [9, 0, 0, 4, 0, 0, 0, 0, 5],
               [7, 0, 0, 0, 0, 9, 0, 0, 0],
               [0, 0, 1, 0, 7, 5, 3, 4, 9],
               [2, 3, 0, 0, 4, 8, 1, 0, 7]]
    solution = [[3, 9, 6, 5, 2, 4, 8, 7, 1],
                [8, 2, 7, 1, 3, 6, 5, 9, 4],
                [5, 1, 4, 8, 9, 7, 6, 2, 3],
                [4, 5, 3, 7, 6, 1, 9, 8, 2],
                [1, 7, 8, 9, 5, 2, 4, 3, 6],
                [9, 6, 2, 4, 8, 3, 7, 1, 5],
                [7, 4, 5, 3, 1, 9, 2, 6, 8],
                [6, 8, 1, 2, 7, 5, 3, 4, 9],
                [2, 3, 9, 6, 4, 8, 1, 5, 7]]
    assert Sudoku(problem).solve() == solution

    problem = [[6, 0, 0, 0, 0, 0, 0, 0, 2],
               [0, 0, 3, 6, 0, 1, 7, 0, 0],
               [0, 7, 0, 0, 4, 0, 0, 1, 0],
               [0, 5, 0, 9, 0, 4, 0, 3, 0],
               [0, 0, 9, 0, 0, 0, 1, 0, 0],
               [0, 6, 0, 7, 0, 8, 0, 2, 0],
               [0, 3, 0, 0, 6, 0, 0, 5, 0],
               [0, 0, 5, 3, 0, 9, 4, 0, 0],
               [7, 0, 0, 0, 0, 0, 0, 0, 3]]
    solution = [[6, 1, 8, 5, 9, 7, 3, 4, 2],
                [4, 9, 3, 6, 2, 1, 7, 8, 5],
                [5, 7, 2, 8, 4, 3, 9, 1, 6],
                [2, 5, 7, 9, 1, 4, 6, 3, 8],
                [3, 8, 9, 2, 5, 6, 1, 7, 4],
                [1, 6, 4, 7, 3, 8, 5, 2, 9],
                [9, 3, 1, 4, 6, 2, 8, 5, 7],
                [8, 2, 5, 3, 7, 9, 4, 6, 1],
                [7, 4, 6, 1, 8, 5, 2, 9, 3]]
    assert Sudoku(problem).solve() == solution

    problem = [[7, 0, 0, 0, 0, 0, 0, 0, 3],
               [0, 0, 3, 1, 0, 5, 7, 0, 0],
               [0, 2, 0, 0, 9, 0, 0, 8, 0],
               [0, 8, 0, 3, 0, 1, 0, 6, 0],
               [0, 0, 1, 0, 0, 0, 8, 0, 0],
               [0, 7, 0, 9, 0, 8, 0, 4, 0],
               [0, 3, 0, 0, 4, 0, 0, 7, 0],
               [0, 0, 7, 5, 0, 2, 9, 0, 0],
               [9, 0, 0, 0, 0, 0, 0, 0, 5]]
    solution = [[7, 5, 9, 2, 8, 4, 6, 1, 3],
                [8, 4, 3, 1, 6, 5, 7, 9, 2],
                [1, 2, 6, 7, 9, 3, 5, 8, 4],
                [5, 8, 4, 3, 7, 1, 2, 6, 9],
                [3, 9, 1, 4, 2, 6, 8, 5, 7],
                [6, 7, 2, 9, 5, 8, 3, 4, 1],
                [2, 3, 5, 8, 4, 9, 1, 7, 6],
                [4, 6, 7, 5, 1, 2, 9, 3, 8],
                [9, 1, 8, 6, 3, 7, 4, 2, 5]]
    assert Sudoku(problem).solve() == solution

    problem = [[0, 0, 6, 3, 0, 0, 0, 0, 2],
               [0, 3, 0, 0, 4, 0, 0, 6, 0],
               [7, 0, 0, 0, 0, 1, 9, 0, 0],
               [2, 0, 0, 0, 0, 8, 7, 0, 0],
               [0, 1, 0, 0, 5, 0, 0, 4, 0],
               [0, 0, 9, 1, 0, 0, 0, 0, 5],
               [0, 0, 7, 4, 0, 0, 0, 0, 8],
               [0, 9, 0, 0, 1, 0, 0, 2, 0],
               [3, 0, 0, 0, 0, 5, 6, 0, 0]]
    solution = [[1, 5, 6, 3, 8, 9, 4, 7, 2],
                [9, 3, 2, 5, 4, 7, 8, 6, 1],
                [7, 8, 4, 2, 6, 1, 9, 5, 3],
                [2, 4, 5, 9, 3, 8, 7, 1, 6],
                [8, 1, 3, 7, 5, 6, 2, 4, 9],
                [6, 7, 9, 1, 2, 4, 3, 8, 5],
                [5, 6, 7, 4, 9, 2, 1, 3, 8],
                [4, 9, 8, 6, 1, 3, 5, 2, 7],
                [3, 2, 1, 8, 7, 5, 6, 9, 4]]
    assert Sudoku(problem).solve() == solution

    problem = [[0, 7, 0, 0, 3, 0, 0, 5, 0],
               [0, 0, 0, 9, 0, 2, 0, 0, 0],
               [1, 0, 6, 0, 0, 0, 4, 0, 2],
               [0, 0, 4, 0, 0, 0, 8, 0, 0],
               [7, 0, 0, 0, 4, 0, 0, 0, 5],
               [0, 0, 1, 0, 0, 0, 6, 0, 0],
               [8, 0, 5, 0, 0, 0, 7, 0, 3],
               [0, 0, 0, 8, 0, 9, 0, 0, 0],
               [0, 6, 0, 0, 7, 0, 0, 1, 0]]
    solution = [[2, 7, 8, 1, 3, 4, 9, 5, 6],
                [4, 5, 3, 9, 6, 2, 1, 8, 7],
                [1, 9, 6, 5, 8, 7, 4, 3, 2],
                [6, 2, 4, 3, 9, 5, 8, 7, 1],
                [7, 8, 9, 6, 4, 1, 3, 2, 5],
                [5, 3, 1, 7, 2, 8, 6, 4, 9],
                [8, 4, 5, 2, 1, 6, 7, 9, 3],
                [3, 1, 7, 8, 5, 9, 2, 6, 4],
                [9, 6, 2, 4, 7, 3, 5, 1, 8]]
    assert Sudoku(problem).solve() == solution

    problem = [[9, 0, 0, 0, 4, 0, 0, 0, 6],
               [0, 0, 5, 2, 0, 0, 4, 0, 0],
               [0, 3, 0, 0, 1, 0, 0, 5, 0],
               [0, 0, 0, 0, 0, 0, 0, 8, 0],
               [3, 0, 4, 0, 9, 0, 7, 0, 5],
               [0, 7, 0, 0, 0, 0, 0, 0, 0],
               [0, 2, 0, 0, 3, 0, 0, 1, 0],
               [0, 0, 8, 0, 0, 6, 3, 0, 0],
               [6, 0, 0, 0, 7, 0, 0, 0, 9]]
    solution = [[9, 8, 1, 7, 4, 5, 2, 3, 6],
                [7, 6, 5, 2, 8, 3, 4, 9, 1],
                [4, 3, 2, 6, 1, 9, 8, 5, 7],
                [2, 5, 9, 4, 6, 7, 1, 8, 3],
                [3, 1, 4, 8, 9, 2, 7, 6, 5],
                [8, 7, 6, 3, 5, 1, 9, 4, 2],
                [5, 2, 7, 9, 3, 4, 6, 1, 8],
                [1, 9, 8, 5, 2, 6, 3, 7, 4],
                [6, 4, 3, 1, 7, 8, 5, 2, 9]]
    assert Sudoku(problem).solve() == solution
    problem = [[2, 0, 8, 3, 4, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 7, 1, 0, 0],
               [4, 0, 0, 0, 0, 0, 0, 0, 7],
               [0, 0, 0, 0, 7, 5, 3, 6, 0],
               [0, 3, 0, 0, 0, 0, 2, 0, 0],
               [5, 0, 0, 1, 0, 0, 0, 0, 0],
               [1, 0, 0, 8, 0, 0, 0, 0, 0],
               [0, 5, 2, 0, 0, 0, 0, 3, 9],
               [0, 0, 0, 0, 0, 6, 5, 0, 0]]
    solution = [[2, 7, 8, 3, 4, 1, 9, 5, 6],
                [6, 9, 5, 2, 8, 7, 1, 4, 3],
                [4, 1, 3, 5, 6, 9, 8, 2, 7],
                [9, 2, 1, 4, 7, 5, 3, 6, 8],
                [7, 3, 4, 6, 9, 8, 2, 1, 5],
                [5, 8, 6, 1, 3, 2, 7, 9, 4],
                [1, 6, 9, 8, 5, 3, 4, 7, 2],
                [8, 5, 2, 7, 1, 4, 6, 3, 9],
                [3, 4, 7, 9, 2, 6, 5, 8, 1]]
    assert Sudoku(problem).solve() == solution

    problem = [[0, 9, 1, 0, 0, 0, 7, 0, 0],
               [0, 0, 8, 0, 0, 6, 0, 0, 0],
               [0, 0, 6, 0, 4, 3, 0, 2, 0],
               [0, 4, 0, 0, 0, 0, 3, 7, 0],
               [0, 0, 3, 0, 7, 8, 0, 1, 0],
               [0, 0, 0, 0, 9, 0, 0, 8, 0],
               [7, 6, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 9, 0, 0, 0, 0, 4, 0],
               [0, 0, 0, 0, 0, 0, 5, 0, 1]]
    solution = [[4, 9, 1, 2, 8, 5, 7, 6, 3],
                [2, 3, 8, 7, 1, 6, 9, 5, 4],
                [5, 7, 6, 9, 4, 3, 1, 2, 8],
                [8, 4, 5, 6, 2, 1, 3, 7, 9],
                [9, 2, 3, 5, 7, 8, 4, 1, 6],
                [6, 1, 7, 3, 9, 4, 2, 8, 5],
                [7, 6, 4, 1, 5, 9, 8, 3, 2],
                [1, 5, 9, 8, 3, 2, 6, 4, 7],
                [3, 8, 2, 4, 6, 7, 5, 9, 1]]
    assert Sudoku(problem).solve() == solution

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
    assert Sudoku(problem).solve() == solution

    # (INVALID GRID) -----------------------------------------------------------
    problem = [[1, 1, 3, 4, 5, 6, 7, 8, 9],  # 1, 1 is INVALID
               [4, 0, 6, 7, 8, 9, 1, 2, 3],
               [7, 8, 9, 1, 2, 3, 4, 5, 6],
               [2, 3, 4, 5, 6, 7, 8, 9, 1],
               [5, 6, 7, 8, 9, 1, 2, 3, 4],
               [8, 9, 1, 2, 3, 4, 5, 6, 7],
               [3, 4, 5, 6, 7, 8, 9, 1, 2],
               [6, 7, 8, 9, 1, 2, 3, 4, 5],
               [9, 1, 2, 3, 4, 5, 6, 7, 8]]
    # fixme: should throw an error but does not
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')


    problem = [[1, 2, 3, 4, 5, 6, 7, 8, 9],  # col 0: 1,1 INVALID
               [1, 0, 6, 7, 8, 9, 1, 2, 3],
               [7, 8, 9, 1, 2, 3, 4, 5, 6],
               [2, 3, 4, 5, 6, 7, 8, 9, 1],
               [5, 6, 7, 8, 9, 1, 2, 3, 4],
               [8, 9, 1, 2, 3, 4, 5, 6, 7],
               [3, 4, 5, 6, 7, 8, 9, 1, 2],
               [6, 7, 8, 9, 1, 2, 3, 4, 5],
               [9, 1, 2, 3, 4, 5, 6, 7, 8]]
    # fixme should throw an error
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

    problem = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
               [4, 0, 6, 7, 8, 9, 1, 2, 3],
               [7, 8, 1, 1, 2, 3, 4, 5, 6],  # 1, 1 in the fixed values
               [2, 3, 4, 5, 6, 7, 8, 9, 1],
               [5, 6, 7, 8, 9, 1, 2, 3, 4],
               [8, 9, 1, 2, 3, 4, 5, 6, 7],
               [3, 4, 5, 6, 7, 8, 9, 1, 2],
               [6, 7, 8, 9, 1, 2, 3, 4, 5],
               [9, 1, 2, 3, 4, 5, 6, 7, 8]]
    # fixme: should through an error
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

    problem = [[1, 1, 3, 4, 5, 6, 7, 8, 9],
               [4, 0, 6, 7, 8, 9, 1, 2, 3],
               [7, 8, 9, 1, 2, 3, 4, 5, 6],
               [2, 3, 4, 5, 6, 7, 8, 9],
               [5, 6, 7, 8, 9, 1, 2, 3, 4],
               [8, 9, 1, 2, 3, 4, 5, 6, 7],
               [3, 4, 5, 6, 7, 8, 9, 1, 2],
               [6, 7, 8, 9, 1, 2, 3, 4, 5],
               [9, 1, 2, 3, 4, 5, 6, 7, 8]]
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

    problem = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
               [4, 0, 6, 7, 8, 9, 1, 2, 3],
               [7, 8, 9, 1, 2, 3, 4, 5, 6],
               [2, 3, 4, 5, 6, 7, 8, 9, 1],
               [5, 6, 7, 8, 9, 1, 2, 3, 4],
               [8, 9, 1, 2, 3, 4, 5, 6, 7],
               [3, 4, 5, 6, 7, 8, 9, 1, 2],
               [6, 7, 8, 9, 1, 2, 3, 4, 5]]
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

    problem = [[1, 2, 3, 4, 5, 6, 7, 8],
               [4, 0, 6, 7, 8, 9, 1, 2],
               [7, 8, 9, 1, 2, 3, 4, 5],
               [2, 3, 4, 5, 6, 7, 8, 9],
               [5, 6, 7, 8, 9, 1, 2, 3],
               [8, 9, 1, 2, 3, 4, 5, 6],
               [3, 4, 5, 6, 7, 8, 9, 1],
               [6, 7, 8, 9, 1, 2, 3, 4],
               [9, 1, 2, 3, 4, 5, 6, 7]]
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

    problem = [[1, 2, 3, 4, 5, 6, 7, 8, 'a'],
               [4, 0, 6, 7, 8, 9, 1, 2, 3],
               [7, 8, 9, 1, 2, 3, 4, 5, 6],
               [2, 3, 4, 5, 6, 7, 8, 9, 1],
               [5, 6, 7, 8, 9, 1, 2, 3, 4],
               [8, 9, 1, 2, 3, 4, 5, 6, 7],
               [3, 4, 5, 6, 7, 8, 9, 1, 2],
               [6, 7, 8, 9, 1, 2, 3, 4, 5],
               [9, 1, 2, 3, 4, 5, 6, 7, 8]]
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

    problem = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 2, 3, 4, 5, 6, 7, 8, 9],
               [1, 2, 3, 4, 5, 6, 7, 8, 9]]
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

    problem = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
               [2, 2, 2, 2, 2, 2, 2, 2, 2],
               [3, 3, 3, 3, 3, 3, 3, 3, 3],
               [4, 4, 4, 4, 4, 4, 4, 4, 4],
               [5, 5, 5, 5, 5, 5, 5, 5, 5],
               [6, 6, 6, 6, 6, 6, 6, 6, 6],
               [7, 7, 7, 7, 7, 7, 7, 7, 7],
               [8, 8, 8, 8, 8, 8, 8, 8, 8],
               [9, 9, 9, 9, 9, 9, 9, 9, 9]]
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

    problem = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
               [2, 3, 4, 5, 6, 7, 8, 9, 1],
               [3, 4, 5, 6, 7, 8, 9, 1, 2],
               [4, 5, 6, 7, 8, 9, 1, 2, 3],
               [5, 6, 7, 8, 9, 1, 2, 3, 4],
               [6, 7, 8, 9, 1, 2, 3, 4, 5],
               [7, 8, 9, 1, 2, 3, 4, 5, 6],
               [8, 9, 1, 2, 3, 4, 5, 6, 7],
               [9, 1, 2, 3, 4, 5, 6, 7, 8]]
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

    problem = [[0, 9, 6, 5, 0, 4, 0, 7, 1],
               [0, 2, 0, 1, 0, 0, 0, 0, 0],
               [0, 1, 4, 0, 9, 0, 6, 2, 3],
               [0, 0, 3, 0, 6, 0, 0, 8, 0],
               [0, 0, 8, 0, 5, 0, 4, 0, 0],
               [9, 0, 0, 4, 1, 0, 0, 0, 5],
               [7, 0, 0, 0, 0, 9, 0, 0, 0],
               [0, 0, 1, 0, 7, 5, 3, 4, 9],
               [2, 3, 0, 0, 4, 8, 1, 0, 7]]
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')

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
    try:
        Sudoku(problem).solve()
        print('failed to fail')
    except:
        print('successfull test')



