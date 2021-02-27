from copy import deepcopy

from Sudoku.Board.BlockView import BlockView, ColumnView


class Experiment:
    def __init__(self, sudoku):
        self.board = deepcopy(sudoku.problem)
        self.blockview = BlockView(self.problem)
        self.columnview = ColumnView(self.problem)

        # TODO move zeros to Sudoku
        self.zeros = [(r, c) for r, row in enumerate(self.board) for c, v in enumerate(row) if v == 0]
        self.unvisited = list(self.zeros)  # create a copy for second run
        self.remaining_choices = []

    def options(self, r, c):
        """at position (r, c) in the sudoku, which are the current applicable choices"""
        b = self.blockindex(r, c)
        rs, cs, bs = set(self.problem[r]), set(self.columnview[c]), set(self.blockview[b])
        return self.values.difference(rs.union(cs, bs))

    def nextzero(self):
        """yield the next zero to choose from."""
        return self.unvisited.pop(0)
