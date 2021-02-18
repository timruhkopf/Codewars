


class StrategyStack:

    def execute(board, row):
        """
        TODO briefly describe the strategy
        :param row:
        """
        StrategyStack.update_2ndstage(board, row)

    def update_2ndstage(board, row):
        """
        recursive solving for the last remaining ambiguous case
        :param row:
        """
        for choice in board.downtown_row[row]:
            # notice the dependence to ._update_det
            stack = StrategyStack._update_det(pos1=board.downtown_row, fix=[set([v]) for v in choice], col=row)
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
        """# TODO """
        for k, v in stack.items():
            board.downtown_row[k].extend(v)

    def _update_det(board, pos1, fix, col):  # TODO refactor name
        """update deterministics across "columns" & early stopping!"""
        uniques = list((i, v) for i, v in enumerate(fix) if len(v) == 1)
        stack = {k: [] for k in range(board.probsize)}
        for j in {*range(board.probsize)} - {col}:
            for tup in pos1[j]:
                for i, v in uniques:
                    if tup[i] in v:
                        pos1[j].remove(tup)
                        stack[j].append(tup)
                        break
        return stack  # relevant only for last 7*7er case
