from collections import deque

from ..Board.Experiment import Experiment


class Strategyforwardbackward:
    def execute(sudoku):
        """Strategy is a composite of Experiment, forward & backNforth.
        Experiment is the 'guidance' i.e. which zero to look next to and what options are
        available given the boards state.
        forward is a recursive backtracker, that lazily evaluates the options
        and moves FORWARD until all zeros are filled (or no solution was found).
        Notice, that forward communicates to Experiment all the remaining options
        at the end of the recursive path. (going back)
        Given a Solution was found, backNforth starts at the last zero position
        on the full board., sets it
        to zero and looks at the remaining options ; if none available, it moves up,
        sets that value to zero and looks at its options. once non-empty (remaining-)
        options were found, it checks the options for their validity. Moving the
        regular forward path again. If the options did not pose a viable solution,
        the path backwards is continued one step back."""

        # (1) First Execution find a Solution
        experiment = Experiment(sudoku.problem, sudoku.zeros)
        r, c = experiment.nextzero()
        options = experiment.options(r, c)
        Strategyforwardbackward.forward(experiment, r, c, options)

        success = Strategyforwardbackward.append_solution(sudoku, experiment)
        if success:
            # early stopping - if no solution was found next algo will not be executed
            return None

        # (2) Second Execution figure out if there is another Solution
        experiment.unvisited = deque(reversed(sudoku.zeros))
        Strategyforwardbackward.backNforth(experiment)

        # check recursion found a solution. solutions are guaranteed to be valid.
        # notice: since forward options.pop, the second solution will never be the same as first
        Strategyforwardbackward.append_solution(sudoku, experiment)

    def append_solution(sudoku, experiment):
        # check recursion found a solution. solutions are guaranteed to be valid.
        if not any([row.count(0) for row in experiment.problem]):
            sudoku.solutions.append(experiment.problem)
            return True
        else:
            return False

    def forward(experiment, r, c, options):
        """forward path with recursive backtracking:
        given a position figure out the applicable choices for that position;
        try one out and see what the next position's choices are - if it has no choice
        - or no choice, that recursively yields a solution, try the next applicable option.
        This algorithm tracks how many options are available"""

        while bool(options):
            choice = options.pop()
            experiment.problem[r][c] = choice

            # (0) BASECASE no zeros on the board
            if not bool(experiment.unvisited):
                experiment.problem[r][c] = choice
                # experiment.remaining_choices[(r, c)] = options  # tracking for the second run # todo remove?
                return True

            # (1) recursive continuation:
            newr, newc = experiment.nextzero()
            newoptions = experiment.options(newr, newc)
            if Strategyforwardbackward.forward(experiment, newr, newc, newoptions):  # recursion
                experiment.remaining_choices[(r, c)] = options  # tracking for the second run
                return True

            else:
                continue

        else:
            # (3) no options are applicable: return to higher hierarchy level
            experiment.unvisited.appendleft((r, c))  # counters nextzero()
            experiment.problem[r][c] = 0
            return False

    def backNforth(experiment):
        """Given the board was solved with the StrategyPosition.forward -
        a stack of the remaining_options for a position is available - look for another solution.
        This is efficiently done by walking through the stack in reverse and trying out
        the remaining options (from each option: go forward). make early stopping available;
        once a single solution is found, stop the entire execution"""

        flag = False
        while bool(experiment.remaining_choices):
            r, c = experiment.nextzero()
            options = experiment.remaining_choices.pop((r, c))
            while bool(options):
                choice = options.pop(0)
                experiment.board[r][c] = choice

                # now go forward again from this choice:
                r, c = experiment.nextzero()
                newoption = experiment.options(r, c)
                if Strategyforwardbackward.forward(experiment, r, c, newoption):
                    flag = True
                    break  # does break hinder while-else branch to execute?

            else:
                # set this position to 0 and move up in the options 'stack'
                experiment.board[r][c] = 0

            if flag:
                # exit the outer while - if a (second) solution was found
                break
