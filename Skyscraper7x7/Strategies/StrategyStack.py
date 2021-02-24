from Skyscraper7x7.Solver.Solution import Solution


class StrategyStack:

    def execute(board):
        """
        TODO briefly describe the strategy

        strategy only relevant for 7x7 medved case
        :param row: index of
        """

        # TODO Refactor these attributes & the stack to a seperate object?
        # helper variables needed across the recursion
        board.column_sets = [set() for i in range(len(board.downtown_row))]
        board.bench = set(range(1, board.probsize + 1))
        board.unvisited = set(range(board.probsize))

        # Consider choosing shortest set of permutations as initialisation:
        # row = min(((k, len(v)) for k, v in board.downtown_row.items()), key=lambda k, v: v)
        # this required to change call "StrategyStack.backtracking_update(board, row + 1):" in
        # backtracking_update
        StrategyStack.backtracking_update(board, StrategyStack.least_choices(board))

        # remove helper variables
        del board.column_sets
        del board.bench
        del board.unvisited

    def least_choices(board):
        """among those unvistied rows return the index of the one with the least choices"""
        return min(board.downtown_row, key=lambda k: len(board.downtown_row[k]) if k in board.unvisited else 999)

    def backtracking_update(board, row):
        board.unvisited.remove(row)
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
                stack = StrategyStack._update_and_track(
                    board,
                    downtown_=board.downtown_row,
                    choice=choice,
                    row=row,
                    fix=[set([v, *board.column_sets[i]]) for i, v in enumerate(choice)],
                    exclude={row})  # set(range(0, board.probsize)) - board.unvisited)  # already visited rows
                board.downtown_row[row] = [choice]

                # (2) check if the communication left a row with no choices
                after = [len(row) for row in board.downtown_row.values()]
                if not all(after):
                    StrategyStack._revert(board, stack, choice)
                    continue

                # (3) --BASECASE-- after the update, all rows have only one choice left:
                # move up the recursion stack -> executing (4*)
                # short circuit if a candidate solution was found.
                elif after == [1] * board.probsize:
                    # check the visibility is in accordance with the columnclues
                    if Solution.check_a_valid_solution(board, board.clues):
                        return True

                    else:  # the provided solution was contradicting the column information.
                        StrategyStack._revert(board, stack, choice)
                        continue

                # (4) The choice was valid up until now - if there are more rows to explore, do so (recursively)
                elif bool(board.unvisited):
                    # todo change this condition and subsequent if statement (recursive
                    #  call) - to make smart trials: always choose the next row by the smallest amount
                    #  of choices for that row. (fastest way through the tree?)
                    if StrategyStack.backtracking_update(board, StrategyStack.least_choices(board)):
                        # the latter condition suffices but is more expensive lazy 'and' saves computation

                        # (4*) upward path after successful recursion.
                        return True
                    else:
                        # this level's choice did not succeed in lower recursive layers;
                        # revert it and remove from column information
                        StrategyStack._revert(board, stack, choice)
                        continue

        else:  # (5) None of this level's choices was applicable; try next choice in the
            # higher recursion level.
            board.unvisited.add(row)
            return False

    def _revert(board, stack, choice):
        """recreate the downtown_row state before the latest update from a stack"""
        for k, v in stack.items():
            board.downtown_row[k].extend(v)

        # remove choice from column_sets
        for i, v in enumerate(choice):
            board.column_sets[i].remove(v)

    def _update_and_track(board, downtown_, choice, row, fix, exclude):
        """
        Update the pos1 object in place from the selected fix object with early stopping;
        start with looking at the tuple from the left; if the first position of a pos1's tuple is contained
        in the respective fix position set, this tuple is removed already - otherwise,
        the second position of the tup is teststed against fix's second positin set.
        And so on and so forth.

        Further, a stack object is created & returned which keeps track of all the changes made.
        :param downtown_: downtown_* object; dict: {index: list of candidate tuples}
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
        stack[row] = downtown_[row].copy()
        stack[row].remove(choice)

        for j in {*range(board.probsize)} - exclude:  # update all except for exclueded
            for tup in downtown_[j]:
                for i, v in uniques:
                    if tup[i] in v:
                        downtown_[j].remove(tup)
                        stack[j].append(tup)
                        break
        return stack


if __name__ == '__main__':
    # A simple 4x4 example to ckeck out
    from Skyscraper7x7.Solver.Solver import Skyscraper

    #
    # clues = [2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]
    #
    # sky = Skyscraper(clues)
    # sky.downtown_row = {r: list(sky.pclues[sky.rowclues[r]]) for r in range(sky.probsize)}
    # sky.downtown_col = {c: list(sky.pclues[sky.colclues[c]]) for c in range(sky.probsize)}
    # StrategyStack.execute(sky)
    #
    # provided = tuple(tuple(sky.downtown_row[i][0]) for i in range(sky.probsize))
    # solution = ((3, 4, 2, 1),
    #             (1, 2, 3, 4),
    #             (2, 1, 4, 3),
    #             (4, 3, 1, 2))
    #
    # assert solution == provided

    clues = (0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0)

    sky = Skyscraper(clues)
    sky.downtown_row = {r: list(sky.pclues[sky.rowclues[r]]) for r in range(sky.probsize)}
    sky.downtown_col = {c: list(sky.pclues[sky.colclues[c]]) for c in range(sky.probsize)}
    StrategyStack.execute(sky)

    provided = tuple(tuple(sky.downtown_row[i][0]) for i in range(sky.probsize))
    solution = ((2, 1, 4, 3), (3, 4, 1, 2), (4, 2, 3, 1), (1, 3, 2, 4))

    assert solution == provided
