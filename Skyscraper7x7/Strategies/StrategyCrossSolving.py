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


class StrategyCrossSolving:

    @relentless
    def execute(board):
        """TODO describe strategy briefly
        sorting to find the most informative clues (shortest sets)"""
        for row in sorted(range(board.probsize), key=lambda i: len(board.downtown_row[i])):
            StrategyCrossSolving.intersect_update(board, row, margin=0)

        for col in sorted(range(board.probsize), key=lambda i: len(board.downtown_col[i])):
            StrategyCrossSolving.intersect_update(board, col, margin=1)

    def intersect_update(board, col, margin=1):  # TODO refactor name
        """
        # TODO add description
        :param col: int. index of the row / column, on which's basis the intersect_update
        of the respective opposite downtown_*s is produced
        :param margin: int. intersect_update of downtown_row based on downtown_col for margin== 1,
         reverse if margin == 0
        :return: None
        """

        # flip the cross; either row updates the columns or vice versa:
        # rename pos1, pos2 updater, updatee
        updater = (board.downtown_row, board.downtown_col)[margin]
        updatee = (board.downtown_row, board.downtown_col)[margin - 1]

        # TODO Move comment to docstring
        # updating rows independently based on column
        # take all permutations of a e.g. row clue (which is a nested list == a matrix)
        # and for each column build the set of values contained in it.
        # these are the values, that are allowed at the column clue's respective index
        # position.
        fix = [set(column) for column in zip(*updater[col])]
        for i, valid in enumerate(fix):
            updatee[i] = [tup for tup in updatee[i] if tup[col] in valid]

        # create a stack of the removals, that can be added lateron for larger problems
        # TODO make this optional for efficiency (only ambigious problems need stack)
        #  move it to decorator of update?
        # TODO : check if this actually does something - since it does not have inplace changes!
        #  ---> uncertain if it is needed for 7x7 medved case
        # StrategyStack._update_and_track(board, pos1, fix, col)
