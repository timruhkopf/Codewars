class StrategyStack:

    def execute(board, row):
        """
        TODO briefly describe the strategy

        strategy only relevant for 7x7 medved case
        :param row:
        """
        board.column_sets = [set() for i in range(len(board.downtown_row))]
        StrategyStack.backtracking_update(board, row)
        del board.column_sets

    def backtracking_update(board, row):
        """
        recursive (backtracking) solving for the medved case;
        successively try out all permutations in downtown_row[row] for validity.
        Doing so implies inplace changes on the downtown_row object.
        As some recursive selections may proof invalid, a stack is created to
        track the changes made and allow reverting from the stack.
        :param row: index of the row, whose downtown_row is selected from.
        """
        for choice in board.downtown_row[row]:
            # FIXME: progressively choosing in this manner on *_row alone does not ensure that
            #   the columns of the board will also be the unique set of range(1, 8).
            #   keep track of the columns: whenever a tuple is chosen, add its skyscraper
            #   to a list of sets [{}, {}, {}, {}, {}, {}, {}] that contains the previous'
            #   choices values for the repesctive positions.
            #   should a choice have a value that is already contained in the respective
            #   set, continue the for loop. If the for loop ends without any valid candidate,
            #   revert the choice in the previous recursion call and continue.
            #   a revert also must include removing the choice from this list of sets.

            stack = StrategyStack._update_and_track(
                board, pos1=board.downtown_row, fix=[set([v]) for v in choice], col=row)
            board.downtown_row[row] = [choice]

            # determine how many combinations are left in the dictionary for that row
            after = [len(row) for row in board.downtown_row.values()]
            if not all(after):
                StrategyStack._revert(board, stack)
                continue

            elif row != board.probsize - 1:  # there are more rows
                if StrategyStack.backtracking_update(board, row + 1):
                    return True
                else:
                    continue

            elif after == [1, 1, 1, 1, 1, 1, 1]:
                return True

        if after != [1, 1, 1, 1, 1, 1, 1]:  # all choices faulty
            StrategyStack._revert(board, stack)
            return False

    def _revert(board, stack):
        """recreate the downtown_row state before the latest update from a stack"""
        for k, v in stack.items():
            board.downtown_row[k].extend(v)

    def _update_and_track(board, pos1, fix, col):  # TODO refactor pos1 name
        """
        Update the pos1 object in place from the selected fix object with early stopping;
        Further, a stack object is created & returned which keeps track of all the changes made.
        :param pos1: downtown_* object; dict: {index: list of candidate tuples}
        :param fix: list of sets, that represent the updater's (i.e. a row) choice.
        e.g. [{2}, {1}, {6}, {4}, {3}, {7}, {5}] which originated from
        :param col:
        :return: stack: dict of lists. key:
        """
        uniques = list((i, v) for i, v in enumerate(fix) if len(v) == 1)
        stack = {k: [] for k in range(board.probsize)}
        for j in {*range(board.probsize)} - {col}:
            for tup in pos1[j]:
                for i, v in uniques:
                    if tup[i] in v:
                        pos1[j].remove(tup)
                        stack[j].append(tup)
                        break
        return stack
