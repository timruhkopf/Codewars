class StrategyStack:

    def execute(board, row):
        """
        TODO briefly describe the strategy

        strategy only relevant for 7x7 medved case
        :param row:
        """
        # helper variables needed across the recursion
        board.column_sets = [set() for i in range(len(board.downtown_row))]
        board.bench = set(range(1, board.probsize + 1))

        # Consider choosing shortest set of permutations as initialisation:
        # row = min(((k, len(v)) for k, v in board.downtown_row.items()), key=lambda k, v: v)
        # this requirex to change call "StrategyStack.backtracking_update(board, row + 1):" in
        # backtracking_update
        StrategyStack.backtracking_update(board, row)

        # remove helper variables
        del board.column_sets
        del board.bench

    def backtracking_update_decomissioned(board, row):
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
            if any(c in s for c, s in zip(choice, board.column_sets)):
                stack = None
                after = None
                continue
            else:
                for i, v in enumerate(choice):
                    board.column_sets[i].add(v)

            stack = StrategyStack._update_and_track(
                board, pos1=board.downtown_row, fix=[set([v]) for v in choice], col=row)
            board.downtown_row[row] = [choice]

            # determine if after update any row has no permutations left
            after = [len(row) for row in board.downtown_row.values()]
            if not all(after):
                StrategyStack._revert(board, stack)
                continue

            elif row != board.probsize - 1:  # there are more rows, where no decision is made for / found
                if StrategyStack.backtracking_update(board, row + 1):  # enter next level of recursion - returns True
                    # only if it succeeded.
                    return True
                else:
                    # this choice did not succeed in lower recursive levels
                    # - remove it from column_sets and move on
                    for i, v in enumerate(choice):
                        board.column_sets[i].remove(v)
                    continue

            elif after == [1, 1, 1, 1, 1, 1, 1]:  # --BASECASE-- move up the recursion stack
                return True

        if after != [1, 1, 1, 1, 1, 1, 1]:
            StrategyStack._revert(board, stack)

            # remove choice from column_sets
            for i, v in enumerate(choice):
                board.column_sets[i].remove(v)
            return False

        else:
            return False

    def _revert(board, stack, choice):
        """recreate the downtown_row state before the latest update from a stack"""
        for k, v in stack.items():
            board.downtown_row[k].extend(v)

        # remove choice from column_sets
        for i, v in enumerate(choice):
            board.column_sets[i].remove(v)

    def backtracking_update(board, row):
        for choice in board.downtown_row[row]:

            # (0) check if the current choice is conflicting with currently available
            # column information derived from already selected choices (in higher recursion levels)
            if any(c in s for c, s in zip(choice, board.column_sets)):
                # it is conflicting - try next choice
                continue

            else:
                # not conflicting; update the available 'column' information
                for i, v in enumerate(choice):
                    board.column_sets[i].add(v)

                # (1) communicate the choice to the board.
                #  update also removes of each subsequent row those values,
                #  that are already placed in the column! - heavily reduces the recursion
                # FIXME: upon hitting  (2, 1, 4, 7, 6, 5, 3) in row 0, this tuple is no longer in the possibilities.
                stack = StrategyStack._update_and_track(
                    board,
                    pos1=board.downtown_row,
                    choice=choice,
                    row=row,
                    fix=[set([v, *board.column_sets[i]]) for i, v in enumerate(choice)],
                    exclude=set(range(row + 1)))  # already chosen rows todo change if 'smart' row choice
                # strategy
                board.downtown_row[row] = [choice]

                # (2) check if the communication left a row with no choices
                after = [len(row) for row in board.downtown_row.values()]
                if not all(after):
                    StrategyStack._revert(board, stack, choice)
                    continue

                # (3) --BASECASE-- after the update, all rows have only one choice left:
                # move up the recursion stack -> executing (4*)
                elif after == [1] * board.probsize:
                    # check if the provided solution is in accordance with the column information
                    b = tuple(tuple(board.downtown_row[i][0]) for i in range(board.probsize))
                    if all([set(vs) == board.bench for vs in zip(*b)]):
                        return True

                    else:  # the provided solution was contradicting the column information.
                        StrategyStack._revert(board, stack, choice)
                        continue

                # (3) The choice was valid up until now - if there are more rows to explore, do so (recursively)
                elif row != board.probsize - 1:
                    # todo change this condition and subsequent if statement (recursive
                    #  call) - to make smart trials: always choose the next row by the smallest amount
                    #  of choices for that row. (fastest way through the tree?)
                    if StrategyStack.backtracking_update(board, row + 1):
                        # (4*) upward path after successful recursion.
                        return True
                    else:
                        # this level's choice did not succeed in lower recursive layers;
                        # revert it and remove from column information
                        StrategyStack._revert(board, stack, choice)
                        continue

        else:  # (5) None of this level's choices was applicable; try next choice in the
            # higher recursion level.
            return False

    def _update_and_track(board, pos1, choice, row, fix, exclude):  # TODO refactor pos1 name
        """
        Update the pos1 object in place from the selected fix object with early stopping;
        start with looking at the tuple from the left; if the first position of a pos1's tuple is contained
        in the respective fix position set, this tuple is removed already - otherwise,
        the second position of the tup is teststed against fix's second positin set.
        And so on and so forth.

        Further, a stack object is created & returned which keeps track of all the changes made.
        :param pos1: downtown_* object; dict: {index: list of candidate tuples}
        :param choice: list/tuple of int; the chosen permutation
        :param row: index of the row, where choice was chosen
        :param fix: list of sets, that represent the updater's (i.e. a row) choice.
        e.g. [{2}, {1}, {6}, {4}, {3}, {7}, {5}] which originated from
        :param exclude: set of indices in downtown_* that are not to be updated
        :return: stack: dict of lists. key: downtown_row key. value: list of removed candidate tuples
        """
        # deselect comparsions, with empty sets (nothing to remove, cause nothing
        # is known in fix for that position (partial updates are possible)
        uniques = list((i, v) for i, v in enumerate(fix) if len(v) > 0)
        stack = {k: [] for k in range(board.probsize)}
        stack[row] = pos1[row].copy()
        stack[row].remove(choice)

        for j in {*range(board.probsize)} - exclude:  # update all except for exclueded
            for tup in pos1[j]:
                for i, v in uniques:
                    if tup[i] in v:
                        pos1[j].remove(tup)
                        stack[j].append(tup)
                        break
        return stack


if __name__ == '__main__':
    # A simple 4x4 example to ckeck out
    from Skyscraper7x7.Solver.Solver import Skyscraper

    clues = [2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]

    sky = Skyscraper(clues)
    sky.downtown_row = {r: list(sky.pclues[sky.rowclues[r]]) for r in range(sky.probsize)}
    sky.downtown_col = {c: list(sky.pclues[sky.colclues[c]]) for c in range(sky.probsize)}
    StrategyStack.execute(sky, row=0)

    provided = tuple(tuple(sky.downtown_row[i][0]) for i in range(sky.probsize))
    solution = ((3, 4, 2, 1),
                (1, 2, 3, 4),
                (2, 1, 4, 3),
                (4, 3, 1, 2))

    assert solution == provided
