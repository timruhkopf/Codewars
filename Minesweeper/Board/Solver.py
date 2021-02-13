from .Game import Game


class Solver(Game):

    def __init__(self, board, n, context):
        """TODO: write subclassing allows to play Game as a user without and to have multiple solver flavour"""
        super(self).__init__(self, board, n, context)

    def solve(self):
        StrategyOpenZero.execute(self)
        # StrategyZeroAnreiner.execute(self)

        # todo if solvable!
        return self.board
