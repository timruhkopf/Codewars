from collections import deque  # just to have a heap convention

from Sudoku.util import timeit, count_calls


class Strategyforwardbackward:

    @timeit
    def execute(sudoku):
        """Strategy is a composite of sudoku, forward & backNforth.
        sudoku is the 'guidance' i.e. which zero to look next to and what options are
        available given the boards state.
        forward is a recursive backtracker, that lazily evaluates the options
        and moves FORWARD until all zeros are filled (or no solution was found).
        Notice, that forward communicates to sudoku all the remaining options
        at the end of the recursive path. (going back)
        Given a Solution was found, backNforth starts at the last zero position
        on the full board., sets it
        to zero and looks at the remaining options ; if none available, it moves up,
        sets that value to zero and looks at its options. once non-empty (remaining-)
        options were found, it checks the options for their validity. Moving the
        regular forward path again. If the options did not pose a viable solution,
        the path backwards is continued one step back."""

        # (1) First Execution find a Solution
        r, c = sudoku.nextzero()
        options = sudoku.options(r, c)
        Strategyforwardbackward.forward(sudoku, r, c, options)
        print('no.calls to forward:', Strategyforwardbackward.forward.calls)

        # early stopping - if no solution was found next algo will not be executed
        if not sudoku.append_solution():
            raise ValueError('Unsolvable Board')

        # (2) Second Execution figure out if there is another Solution
        sudoku.unvisited = deque(reversed(sudoku.zeros))
        Strategyforwardbackward.backNforth(sudoku)

        # check recursion found a solution. solutions are guaranteed to be valid.
        # notice: since forward options.pop, the second solution will never be the same as first
        sudoku.append_solution()

    @count_calls
    def forward(sudoku, r, c, options):
        """forward path with recursive backtracking:
        given a position figure out the applicable choices for that position;
        try one out and see what the next position's choices are - if it has no choice
        - or no choice, that recursively yields a solution, try the next applicable option.
        This algorithm tracks how many options are available"""

        while bool(options):
            choice = options.pop()
            sudoku.problem[r][c] = choice

            # (0) BASECASE no zeros on the board
            if not bool(sudoku.unvisited):
                sudoku.problem[r][c] = choice
                sudoku.remaining_choices[(r, c)] = options  # tracking for the second run
                return True

            # (1) recursive continuation:
            newr, newc = sudoku.nextzero()
            newoptions = sudoku.options(newr, newc)
            if Strategyforwardbackward.forward(sudoku, newr, newc, newoptions):  # recursion
                sudoku.remaining_choices[(r, c)] = options  # tracking for the second run
                return True

            else:
                continue

        else:
            # (3) no options are applicable: return to higher hierarchy level
            sudoku.unvisited.appendleft((r, c))  # counters nextzero()
            sudoku.problem[r][c] = 0
            return False

    @timeit
    def backNforth(sudoku):
        """Given the board was solved with the StrategyPosition.forward -
        a stack of the remaining_options for a position is available - look for another solution.
        This is efficiently done by walking through the stack in reverse and trying out
        the remaining options (from each option: go forward). make early stopping available;
        once a single solution is found, stop the entire execution"""

        flag = False
        while bool(sudoku.remaining_choices):
            r, c = sudoku.nextzero()
            options = sudoku.remaining_choices.pop((r, c))
            while bool(options):
                choice = options.pop()
                sudoku.problem[r][c] = choice

                # now go forward again from this choice:
                r, c = sudoku.nextzero()
                newoption = sudoku.options(r, c)
                if Strategyforwardbackward.forward(sudoku, r, c, newoption):
                    flag = True
                    break  # does break hinder while-else branch to execute?

            else:
                # set this position to 0 and move up in the options 'stack'
                sudoku.problem[r][c] = 0

            if flag:
                # exit the outer while - if a (second) solution was found
                break
