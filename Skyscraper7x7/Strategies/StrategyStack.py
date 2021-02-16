from .Strategy2 import Strategy2


class StrategyStack:

    def execute(board, row):
        StrategyStack.update_2ndstage(board, row)

    def update_2ndstage(board, row):
        """recursive solving for the last remaining ambigous case"""
        for choice in board.downtown_row[row]:
            # notice the dependence to ._update_det
            stack = Strategy2._update_det(pos1=board.downtown_row, fix=[set([v]) for v in choice], col=row)
            board.downtown_row[row] = [choice]

            # determine how many combinations are left in the dictionary for that row
            after = [len(row) for row in board.downtown_row.values()]
            if not all(after):
                StrategyStack._revert(board, stack)
                continue

            elif row != board.probsize - 1:  # there are more rows
                if StrategyStack.update_2ndstage(row + 1):
                    return True
                else:
                    continue

            elif after == [1, 1, 1, 1, 1, 1, 1]:
                return True

        if after != [1, 1, 1, 1, 1, 1, 1]:  # all choices faulty
            StrategyStack._revert(board, stack)
            return False

    def _revert(board, stack):
        for k, v in stack.items():
            board.downtown_row[k].extend(v)
