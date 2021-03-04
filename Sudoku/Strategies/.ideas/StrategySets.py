import time


# TODO create a Tracker object for sets
class Bookkeeper:
    def __init__(self):
        B = [set(self.problem[r][c] for r, c, b in self.sudokuindex
                 if self.problem[r][c] != 0 and b == i) for i in range(9)]

        self.candblock = [set(range(1, 10)) - block for block in B]
        self.candrow = [set(range(10)) - set(row) for row in self.problem]
        self.candcol = [set(range(10)) - set(column) for column in list(zip(*self.problem))]  # make use of transpose

        self.zeros = [(r, c, b) for r, c, b in self.sudokuindex if self.problem[r][c] == 0]
        self.memo = dict()


class StrategySets:
    """Deprec. Was working, but to slow on the second path"""
    def execute(board):
        t1 = time.time()
        StrategySets._solve_single(position=board.zeros[0], current_idx=0, reverse=False)
        t2 = time.time()
        print('solve_single 1st ', str(t2 - t1))

        solution = board.solution
        if solution == board.problem:
            raise ValueError('InvalidSolution: Unsolvable Sudoku')

        second = Sudoku(board.problem)
        t1 = time.time()
        second._solve_single(board.zeros[0], current_idx=0, reverse=True)

        t2 = time.time()
        print('solve_single 2nd ', str(t2 - t1))
        print('')

        if solution != second.solution:
            raise ValueError('InvalidSolution: Sudoku has multiple Solutions')

        return board.solution

    def options(board, r, c, b, reverse=False):
        """returns sorted intersection of possible values at that location"""
        intersect = board.candrow[r] & board.candcol[c] & board.candblock[b]
        return sorted(intersect, reverse=reverse)

    def _solve_single(board, position, current_idx, reverse=False):
        '''
        recursive path trough the problem,
        whilst considering only applicable paths.
        :returns Single solution, that is the result of traversing on sorted
        options
        '''
        r, c, b = position
        for s in StrategySets.options(*position, reverse):
            if current_idx + 1 == len(board.zeros):  # base case: last zero value is reached
                board.memo[position] = s
                return s
            else:  # go further down on path with current s
                board.memo[position] = s  # DEPREC: REMOVE ME this is only for debug
                board.candrow[r].difference_update({s})
                board.candcol[c].difference_update({s})
                board.candblock[b].difference_update({s})
                sol = board._solve_single(
                    board.zeros[current_idx + 1], current_idx + 1, reverse)

                if bool(sol):  # the next step returned a non empty solution
                    board.memo[position] = s
                    return s

                else:  # the next zero index returns None
                    # i.e. it has no applicable choices: Go up
                    # add s to sets it was removed from
                    board.candrow[r].update({s})
                    board.candcol[c].update({s})
                    board.candblock[b].update({s})
                    if position in board.memo.keys():
                        board.memo.pop(position)
                    continue
        return None
