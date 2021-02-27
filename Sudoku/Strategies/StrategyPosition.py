from copy import deepcopy

from ..Board.Experiment import Experiment


class StrategyPosition:
    def execute(sudoku):

        # (1) First Execution find a Solution
        experiment1 = Experiment(sudoku)
        r, c = experiment1.nextzero()
        options = experiment1.options(r, c)
        StrategyPosition.solve_single(experiment1, r, c, options)

        # check recursion found a solution. solutions are guaranteed to be valid.
        if any([row.count(0) for row in experiment1.board]):
            sudoku.solutions.append(experiment1.board)
        else:
            return None

        # (2) Second Execution figure out if there is another Solution
        experiment2 = Experiment(sudoku)
        experiment2.board = deepcopy(sudoku.solutions[-1])
        experiment2.remaining_choices = experiment1.remaining_choices
        experiment2.unvisited = reversed(experiment1.zeros)
        StrategyPosition.solve_second(experiment2)

        if any([row.count(0) for row in experiment2.board]):
            sudoku.solutions.append(experiment1.board)
        else:
            return None

    def solve_first(experiment, r, c, options):
        """forward path with recursive backtracking:
        given a position figure out the applicable choices for that position;
        try one out and see what the next position's choices are - if it has no choice
        - or no choice, that recursively yields a solution, try the next applicable option.
        This algorithm tracks how many options are available"""

        while bool(options):
            choice = options.pop(0)
            experiment.problem[r][c] = choice

            newr, newc = experiment.nextzero()
            options = experiment.options(newr, newc)
            if StrategyPosition.solve_first(experiment, newr, newc, options):  # recursion
                experiment.remaining_choices[(r, c)] = options  # tracking for the second run
                return True

            elif bool(experiment.unvisited):  # BASECASE no zeros on the board
                experiment.board[r][c] = choice
                experiment.remaining_choices[(r, c)] = options  # tracking for the second run
                return True

            else:
                continue

        else:
            # no options are applicable: return to higher hierarchy level
            experiment.unvisited.leftappend((r, c))
            experiment.board[r][c] = 0
            return False

    def solve_second(experiment):
        """Given the board was solved with the StrategyPosition.solve_first -
        a stack of the remaining_options for a position is available - look for another solution.
        This is efficiently done by walking through the stack in reverse and trying out
        the remaining options (from each option: go forward). make early stopping available;
        once a single solution is found, stop the entire execution"""

        while bool(experiment.remaining_choices):
            options = experiment.remaining_choices.pop()
            while bool(options):
                choice = options.pop(0)
            experiment.board[r][c] = 0

            # now go forward again from this choice:
            r, c = experiment.unvisited.pop(0)  # FIXME: check if valid
            newoption = experiment.options(r, c)
            StrategyPosition.solve_first(experiment, r, c, newoption)
