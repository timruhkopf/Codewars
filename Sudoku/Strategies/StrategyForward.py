from collections import deque  # just to have a heap convention
from copy import deepcopy

from Sudoku.util import timeit, count_calls


class Tracker:
    def __init__(self, sudoku):
        self.unvisited = deque(sudoku.zeros)

    def nextzero(self):
        """yield the next zero to choose from."""
        return self.unvisited.popleft()


class StrategyForward:

    @timeit
    def execute(sudoku):
        """Strategy is a composite of sudoku, forward & backNforth.
        sudoku is the 'guidance' i.e. which zero to look next to and what options are
        available given the boards state.
        forward is a recursive backtracker, that lazily evaluates the options
        and moves FORWARD until all zeros are filled (or no solution was found).
        Notice, that forward communicates to sudoku all the remaining options
        at the end of the recursive path. (going back)
        # TODO UPDATE DOC"""

        # (1) First Execution find a Solution
        tracker = Tracker(sudoku)
        r, c = tracker.nextzero()
        options = sudoku.options(r, c)
        StrategyForward.forward(sudoku, tracker, r, c, options)
        print('no.calls to forward:', StrategyForward.forward.calls)

    @count_calls
    def forward(sudoku, tracker, r, c, options):
        """forward path with recursive backtracking:
        given a position figure out the applicable choices for that position;
        try one out and see what the next position's choices are - if it has no choice
        - or no choice, that recursively yields a solution, try the next applicable option.
        This algorithm tracks how many options are available"""

        while bool(options):
            choice = options.pop()
            sudoku.problem[r][c] = choice

            # (0) BASECASE no zeros on the board
            if not bool(tracker.unvisited):
                sudoku.problem[r][c] = choice
                # write out solution
                return StrategyForward.policy(sudoku, tracker, r, c)

            # (1) recursive continuation:
            newr, newc = tracker.nextzero()
            newoptions = sudoku.options(newr, newc)
            if StrategyForward.forward(sudoku, tracker, newr, newc, newoptions):
                return True
            else:
                continue

        else:
            # (3) no options are applicable: return to higher hierarchy level
            tracker.unvisited.appendleft((r, c))  # counters nextzero()
            sudoku.problem[r][c] = 0
            return False

    def policy(sudoku, tracker, r, c):
        """find a single solution; check for a second solution - raise if a second is found"""
        if not bool(sudoku.solutions):
            sudoku.solutions.append(deepcopy(sudoku.problem))
            tracker.unvisited.appendleft((r, c))
            sudoku.problem[r][c] = 0
            return False
        else:
            raise ValueError('multiple solutions were found')
