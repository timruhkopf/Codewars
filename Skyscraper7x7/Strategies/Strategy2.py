
def relentless(func):
    """method decorator to execute the function until the board no longer changes by the
    method's updates"""

    def wrapper(board, *args):
        state = lambda board: [len(a[i]) for a in (board.downtown_row, board.downtown_col)
                               for i in range(board.probsize)]

        before = []
        after = state(board)
        while before != after:
            before = after
            func(board, *args)
            after = state(board)

    return wrapper


class Strategy2:
    # TODO refactor the classes name

    @relentless
    def execute(board):
        """"""
        for row in sorted(range(board.probsize), key=lambda i: len(board.downtown_row[i])):
            Strategy2.update(row, margin=0)

        for col in sorted(range(board.probsize), key=lambda i: len(board.downtown_col[i])):
            Strategy2.update(col, margin=1)

    def update(board, col, margin=1):
        """column update for margin== 1, rowupdate if margin == 0"""

        pos1 = (board.downtown_row, board.downtown_col)[margin]
        pos2 = (board.downtown_row, board.downtown_col)[margin - 1]

        # updating rows indepenendly based on column
        fix = [set(column) for column in zip(*pos1[col])]
        for i, valid in enumerate(fix):
            pos2[i] = [tup for tup in pos2[i] if tup[col] in valid]

        Strategy2._update_det(pos1, fix, col)

    def _update_det(board, pos1, fix, col):
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
