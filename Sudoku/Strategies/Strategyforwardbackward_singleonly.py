from Sudoku.Strategies.Experiment import Experiment
from Sudoku.Strategies.Strategyforwardbackward import Strategyforwardbackward


class Strategyforwardbackward_single_only:
    def execute(sudoku):
        # TODO move this method to seperate Strategy
        """The (kyu3) kata, that requires only a simple solver (single Solution) - and
        all test cases are guaranteed """

        experiment = Experiment(sudoku.problem, sudoku.zeros)
        r, c = experiment.nextzero()
        options = experiment.options(r, c)
        Strategyforwardbackward.forward(experiment, r, c, options)

        return experiment.problem
