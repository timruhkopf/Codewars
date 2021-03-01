from Sudoku.Strategies.Strategyforwardbackward import Strategyforwardbackward, deque, Tracker


class Strategyforwardbackward_sorted(Strategyforwardbackward):
    def execute_sorted_zeros(sudoku):
        """DEPREC: try to do good decisions early-on: the number of calls to forward is
                by far greater (10x +/-) than in the linear execution. -- this strategy reverts far later,
                as the density of information gain for the next position is smaller """
        experiment = Tracker(sudoku.problem, sudoku.zeros)
        experiment.unvisited = deque(sorted(sudoku.zeros, key=lambda zero: len(experiment.options(*zero))))

        r, c = experiment.nextzero()
        options = experiment.options(r, c)
        Strategyforwardbackward_sorted.forward(experiment, r, c, options)
        print('no.calls to forward:', Strategyforwardbackward_sorted.forward.calls)  # FIXME: this seems a bit high.
