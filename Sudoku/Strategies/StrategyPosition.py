# TODO rather than making expensive set updates that always are statesafe versions of the entire board,
#  make small position dependent inquiries, that on demand determine the current row / col / block sets! and determine
#  the current valid options.

# TODO: make a check functino, that cares only for the current state
#  abandon sets - their updates take tooo damn long for multiple sudoku. Test cases
#  work locally though

class StrategyPosition:
    def execute(board):
        pass
