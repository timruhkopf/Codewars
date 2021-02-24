from Skyscraper7x7.Solver.Solution import Solution


class Bookkeeper:
    def __init__(self, board):
        """Keeps abstract STATE of the algorithm."""
        self.board = board
        self.column_sets = [set() for i in range(len(board.downtown_row))]
        self.bench = set(range(1, board.probsize + 1))
        self.unvisited = set(range(board.probsize))

    @property
    def visited(self):
        return set(range(0, self.board.probsize)) - self.unvisited

    def fixture(self, choice):
        return [set([v, *self.column_sets[i]]) for i, v in enumerate(choice)]

    @property
    def next_row(self):
        row = self.least_choices()
        self.unvisited.remove(row)
        return row

    def least_choices(self):
        """among those unvistied rows return the index of the one with the least choices"""
        return min(self.board.downtown_row,
                   key=lambda k: len(self.board.downtown_row[k]) if k in self.unvisited else 999)


class StrategyStack:
    def execute(board):
        """
        TODO briefly describe the strategy

        strategy only relevant for 7x7 medved case
        :param row: index of
        """

        # TODO Refactor these attributes & the stack to a seperate object?
        # helper variables needed across the recursion
        booki = Bookkeeper(board)
        StrategyStack.backtracking_update(booki, board)

    def backtracking_update(booki, board):
        row = booki.next_row
        for choice in board.downtown_row[row]:

            # (0) check if the current choice is conflicting with currently available
            # column information derived from already selected choices (in higher recursion levels)
            if any(c in s for c, s in zip(choice, booki.column_sets)):
                # it is conflicting - try next choice
                continue

            else:
                # not conflicting; update the available 'column' information
                for i, v in enumerate(choice):
                    booki.column_sets[i].add(v)

                # (1) communicate the choice to the board.
                #  update also removes of each subsequent row those values,
                #  that are already placed in the column! - heavily reduces the recursion
                stack = StrategyStack._update_and_track(
                    board,
                    downtown_=board.downtown_row,
                    choice=choice,
                    row=row,
                    fix=booki.fixture(choice),
                    exclude=booki.visited)  # {row})   # already visited rows
                board.downtown_row[row] = [choice]

                # (2) check if the communication left a row with no choices
                after = [len(row) for row in board.downtown_row.values()]
                if not all(after):
                    StrategyStack._revert(board, booki, stack, choice)
                    continue

                # (3) --BASECASE-- after the update, all rows have only one choice left:
                # move up the recursion stack -> executing (4*)
                # short circuit if a candidate solution was found.
                elif after == [1] * board.probsize:
                    # check the visibility is in accordance with the columnclues
                    if Solution.check_a_valid_solution(board, board.clues):
                        return True

                    else:  # the provided solution was contradicting the column information.
                        StrategyStack._revert(board, booki, stack, choice)
                        continue

                # (4) The choice was valid up until now - if there are more rows to explore, do so (recursively)
                elif bool(booki.unvisited):
                    if StrategyStack.backtracking_update(booki, board):
                        # (4*) upward path after successful recursion.
                        return True
                    else:
                        # this level's choice did not succeed in lower recursive layers;
                        # revert it and remove from column information
                        StrategyStack._revert(board, booki, stack, choice)
                        continue

        else:  # (5) None of this level's choices was applicable; try next choice in the
            # higher recursion level.
            booki.unvisited.add(row)
            return False

    def _revert(board, booki, stack, choice):
        """recreate the downtown_row state before the latest update from a stack"""
        for k, v in stack.items():
            board.downtown_row[k].extend(v)

        # remove choice from column_sets
        for i, v in enumerate(choice):
            booki.column_sets[i].remove(v)

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

    clues = [2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]

    sky = Skyscraper(clues)
    sky.downtown_row = {r: list(sky.pclues[sky.rowclues[r]]) for r in range(sky.probsize)}
    sky.downtown_col = {c: list(sky.pclues[sky.colclues[c]]) for c in range(sky.probsize)}
    StrategyStack.execute(sky)

    provided = tuple(tuple(sky.downtown_row[i][0]) for i in range(sky.probsize))
    solution = ((3, 4, 2, 1),
                (1, 2, 3, 4),
                (2, 1, 4, 3),
                (4, 3, 1, 2))

    assert solution == provided

    clues = (0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0)

    sky = Skyscraper(clues)
    sky.downtown_row = {r: list(sky.pclues[sky.rowclues[r]]) for r in range(sky.probsize)}
    sky.downtown_col = {c: list(sky.pclues[sky.colclues[c]]) for c in range(sky.probsize)}
    StrategyStack.execute(sky)

    provided = tuple(tuple(sky.downtown_row[i][0]) for i in range(sky.probsize))
    solution = ((2, 1, 4, 3), (3, 4, 1, 2), (4, 2, 3, 1), (1, 3, 2, 4))

    assert solution == provided
