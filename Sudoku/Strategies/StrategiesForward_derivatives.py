from .StrategyForward import StrategyForward, Tracker, deque, deepcopy


class StrategyAll(StrategyForward):
    def policy(sudoku, tracker, r, c):
        """find all solutions of the board and append them"""
        sudoku.solutions.append(deepcopy(sudoku.problem))
        tracker.unvisited.appendleft((r, c))
        sudoku.problem[r][c] = 0
        return False


class StrategySingleSolution(StrategyForward):
    def policy(sudoku, tracker, r, c):
        sudoku.solutions.append(deepcopy(sudoku.problem))
        return True


class StrategyOptionSorted(StrategyForward):
    def execute(sudoku):
        """DEPREC: try to do good decisions early-on: the number of calls to forward is
                by far greater (10x +/-) than in the linear execution. -- this strategy reverts far later,
                as the density of information gain for the next position is smaller """
        experiment = Tracker(sudoku.problem, sudoku.zeros)
        experiment.unvisited = deque(sorted(sudoku.zeros, key=lambda zero: len(experiment.options(*zero))))

        StrategyForward.execute(sudoku)
        print('no.calls to forward:', StrategyForward.forward.calls)  # FIXME: this seems a bit high.
