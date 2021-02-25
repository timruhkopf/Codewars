from Skyscraper7x7.Solver.Solution import Solution


class Bookkeeper:
    def __init__(self, board, rowmajor=True):
        """Keeps abstract STATE of the algorithm and provides guidance to it
        as to which row is next to be examined. It also declutters the interface.
        :param rowmajor:"""
        self.board = board
        self.downtown = [board.downtown_col, board.downtown_row][rowmajor]
        # consider set: self.downtown = {k: set(v) for k, v in self.downtown.items()}
        self.clues = board.clues
        self.probsize = board.probsize
        self.column_sets = [set() for i in range(len(self.downtown))]
        self.bench = set(range(1, board.probsize + 1))
        self.unvisited = set(range(board.probsize))

    @property
    def visited(self):
        return set(range(0, self.probsize)) - self.unvisited

    def fixture(self, choice):
        return [set([v, *self.column_sets[i]]) for i, v in enumerate(choice)]

    @property
    def next_row(self):
        row = self.least_choices()
        self.unvisited.remove(row)
        return row

    def least_choices(self):
        """among those unvistied rows return the index of the one with the least choices"""
        return min(self.downtown, key=lambda k: len(self.downtown[k]) if k in self.unvisited else 999)

    def _revert(self, stack, choice):
        """recreate the downtown state before the latest update from a stack"""
        for k, v in stack.items():
            self.downtown[k].extend(v)

        # remove choice from column_sets
        for i, v in enumerate(choice):
            self.column_sets[i].remove(v)


class StrategyStack:

    def execute(board, rowmajor=True):
        """
        This Strategy lives in the context of a bookkeeper object, that declutters its interface and
        keeps track of additional information. Furthermore the bookkeeper provides additional guidance in
        terms of efficiency. The core idea of this algorithm is a recursive trial and error; working
        inplace on board.downtown. Knowing that downtown contains the TRUE choice given the clues,
        it simply tries them out recursively; creating a stack of its actions and reverts them,
        the choice was faulty (either it conflicts with the accumulated column information of its former choices,
        a choice leaves another row with no choices, or if it found a configuration that leaves each
        row with one choice tests it with the boards clues and fails). The inplace update of downtown
        is "smart" i.e. it employs early stopping - a single conflict of a candidate is sufficient to remove
        it from downtown & moves it to the stack. Another "smart" move is guided by the Bookkeeper,
        which determines the next row, that is to be chosen from in the next recursive layer.
        It suggests the next row with the least choices. this way, the algorithm can move quickly through
        the board.

        Notice, this algorithm is a fully fledged solver, that is guaranteed to find the solution eventually
        if all collections in downtown contain the True row solution. Despite the performance tweaks,
        it is highly recommended to reduce the number of available choices.
        The main purpose of this algorithm lies in its ability to find appropriate solutions
        for clues that contain insufficient information; i.e. StrategyCrossSolving left ambiguity.
        This is the case for Skyscraper 7x7 medved testcase.

        :param board: Skyscraper object.
        :param rowmajor: boolean: decides whether the algorithm works on downtown_row or downtown_col
        :returns None: inplace changes are made on board.downtown_*
        """

        self = Bookkeeper(board, rowmajor)
        StrategyStack.backtracking_update(self, row=self.next_row)

    def backtracking_update(self, row):
        for choice in self.downtown[row]:

            # (0) check if the current choice is conflicting with currently available
            # column information derived from already selected choices (in higher recursion levels)
            if any(c in s for c, s in zip(choice, self.column_sets)):
                # it is conflicting - try next choice
                continue

            else:
                # not conflicting; update the available 'column' information
                for i, v in enumerate(choice):
                    self.column_sets[i].add(v)

                # (1) communicate the choice to the board.
                #  update also removes of each subsequent row those values,
                #  that are already placed in the column! - heavily reduces the recursion
                stack = StrategyStack._update_and_track(
                    downtown=self.downtown,
                    choice=choice,
                    row=row,
                    fix=self.fixture(choice),
                    exclude=self.visited)  # {row})   # already visited rows
                self.downtown[row] = [choice]  # consider set: {choice}

                # (2) check if the communication left a row with no choices
                after = [len(row) for row in self.downtown.values()]
                if not all(after):
                    self._revert(stack, choice)
                    continue

                # (3) --BASECASE-- after the update, all rows have only one choice left:
                # move up the recursion stack -> executing (4*)
                # short circuit if a candidate solution was found.
                elif after == [1] * self.probsize:
                    # check the visibility is in accordance with the columnclues
                    if Solution.check_a_valid_solution(self.board, self.clues):
                        return True

                    else:  # the provided solution was contradicting the column information.
                        self._revert(stack, choice)
                        continue

                # (4) The choice was valid up until now - if there are more rows to explore, do so (recursively)
                elif bool(self.unvisited):
                    if StrategyStack.backtracking_update(self, row=self.next_row):
                        # (4*) upward path after successful recursion.
                        return True
                    else:
                        # this level's choice did not succeed in lower recursive layers;
                        # revert it and remove from column information
                        self._revert(stack, choice)
                        continue

        else:  # (5) None of this level's choices was applicable; try next choice in the
            # higher recursion level.
            self.unvisited.add(row)
            return False

    @staticmethod
    def _update_and_track(downtown, choice, row, fix, exclude):
        """
        Update the pos1 object in place from the selected fix object with early stopping;
        start with looking at the tuple from the left; if the first position of a pos1's tuple is contained
        in the respective fix position set, this tuple is removed already - otherwise,
        the second position of the tup is teststed against fix's second positin set.
        And so on and so forth.

        Further, a stack object is created & returned which keeps track of all the changes made.
        :param downtown: downtown_* object; dict: {index: list of candidate tuples}
        :param choice: list/tuple of int; the chosen permutation
        # TODO refactor row name to index and describe
        :param row: index of the row, where choice was chosen
        :param fix: list of sets, that represent the updater's (i.e. a row) choice.
        e.g. [{2}, {1}, {6}, {4}, {3}, {7}, {5}] which originated from
        :param exclude: set of indices in downtown_* that are not to be updated
        :return: stack: dict of lists. key: downtown_row key. value: list of removed candidate tuples
        """
        # deselect comparisons, with empty sets (nothing to remove, cause nothing
        # is known in fix for that position (partial updates are possible)
        probsize = len(downtown)
        stack = {k: [] for k in range(probsize)}
        stack[row] = downtown[row].copy()
        stack[row].remove(choice)

        uniques = list((i, v) for i, v in enumerate(fix) if len(v) > 0)
        for j in {*range(probsize)} - exclude:  # update all except for exclueded
            for tup in downtown[j]:
                for i, v in uniques:
                    if tup[i] in v:
                        downtown[j].remove(tup)
                        stack[j].append(tup)
                        break

        # consider set:
        # for j in {*range(probsize)} - exclude:
        #     removals = set(tup for tup in downtown[j] if any(t in u for t, u in zip(tup, fix)))
        #     stack[j].update(removals)
        #     downtown[j].difference_update(removals)
        return stack
