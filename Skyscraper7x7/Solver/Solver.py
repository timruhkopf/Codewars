from collections import deque
from itertools import permutations

from ..Strategies.StrategyCrossSolving import StrategyCrossSolving
from ..Strategies.StrategyStack import StrategyStack


class Skyscraper:
    # preallocation to make it work lazily with all sizes in one test scenario
    _pclues = {4: None, 6: None, 7: None}

    def __init__(self, clues):
        """
        Solver to
        4*4 Skyscraper: https://www.codewars.com/kata/5671d975d81d6c1c87000022 (kyu 4)
        6*6 Skyscraper: https://www.codewars.com/kata/5679d5a3f2272011d700000d (kyu 2)
        7*7 Skyscraper: https://www.codewars.com/kata/5917a2205ffc30ec3a0000a8 (kyu 1)
        """
        self.clues = clues
        self.probsize = int(len(self.clues) / 4)

        # parse the clues
        colclues, rowclues = self._interpret_clues(self.clues)
        self.colclues = colclues
        self.rowclues = rowclues

    def table(self, downtown):
        """__repr__ helper: prints out a table from the "columnsets" of each position"""
        fix = lambda r: [set(column) for column in zip(*downtown[r])]
        rows = [fix(r) for r in range(self.probsize)]

        max_lens = [max([str(s) for s in row], key=len) for row in zip(*rows)]
        max_lens = [len(x) for x in max_lens]

        S = ''
        for row in rows:
            S += '|'.join('{0:{width}}'.format(str(x), width=y) for x, y in zip(row, max_lens)) + '\n'

        return S

    def __repr__(self):
        """EXPERIMENTAL debug method, prints out tables of downtown_row and downtown_col's
         interpret in a 'columnview' fashion. A row reads as the following:
        given
        downtown_row = {0:[(2, 3, 4, 1),
                           (1, 2, 4, 3),
                           (1, 3, 4, 2)], ...}
        we can build the sets across the column, that represent the row
        [{1, 2}, {2, 3}, {4}, {1, 2, 3}]
         They are the index specific applicable values across all positions.

        Notice, since both tables follow the index of the downtown object,
        the column view is printing the columns in transpose. (which is in
        accordance to the downtown_col object!

        WARNING: an intersection of the sets of downtown_row and downtown_column
        for an index position is not a valid operation, as the other sets in the
        same row / column are not appropriately updated!
        """
        if self.downtown_row is not None and self.downtown_col is not None:
            S = 'Row view\n'
            S += self.table(self.downtown_row) + '\n'
            S += 'Column view\n'
            S += self.table(self.downtown_col)
            return S

    @property
    def pclues(self):
        """property getter ensures, that only when needed, the permutations are ONCE! calculated
        for all problems of the same size,
        :returns dict. describes the visibility of all possible permutations"""
        if self._pclues[self.probsize] is None:
            self._pclues[self.probsize] = self._sort_permutations(self.probsize)
            return self._pclues[self.probsize]
        else:
            return self._pclues[self.probsize]

    def _interpret_clues(self, clues):
        """
        interpret the clues:
        :returns lists of tuples which indicate the full row & col info
        """
        clues = [[clues[j * self.probsize + i] for i in range(self.probsize)] for j in range(4)]
        clues = [clue if i in (0, 1) else list(reversed(clue)) for i, clue in enumerate(clues)]

        colclues = [(clues[0][k], clues[0 + 2][k]) for k in range(self.probsize)]
        rowclues = [(clues[1 + 2][k], clues[1][k]) for k in range(self.probsize)]

        return colclues, rowclues

    @staticmethod
    def _visible(tup):
        """
        :param tup: tuple containing integers that are the stories of the skyscraper.
        :return: how many buildings are visible from the left for this particular tup
        of skyscrapers.
        :example:
        (1,2,3,4) --> 4
        (3,2,1,4) --> 2
        """
        ismax = deque([tup[0]])
        for value in tup:
            if ismax[0] < value:
                ismax.appendleft(value)
        return len(ismax)

    # @timeit
    @staticmethod
    def _sort_permutations(problemsize):
        """sorting the permutations by visibility in both directions, creates a lookup table
        for the clues.
        :returns dict. key: tuple: visibility from left & right (left, right),
        value: set of all tuples, that are the permutations with the corresponding left & right
        visibility.
        """
        permute = set(permutations(range(1, problemsize + 1)))

        # Consider; due to lexicographic ordering in permuations: cut no of permutations to half
        #  permute = [p for p in permutations(range(1,problemsize +1)) if p[0] < p[-1]]
        gen = range(1, problemsize + 1)
        pclues = {(k0, k1): set() for k0 in gen for k1 in gen}
        for tup in permute:
            fward = Skyscraper._visible(tup)
            bward = Skyscraper._visible(tup[::-1])

            pclues[(fward, bward)].add(tup)

        pclues.update({(0, k): set.union(*(pclues[(i, k)] for i in gen)) for k in gen})  # supersets
        pclues.update({(k, 0): set.union(*(pclues[(k, i)] for i in gen)) for k in gen})
        pclues = {k: v for k, v in pclues.items() if len(v) != 0}
        pclues.update({(0, 0): permute})
        return pclues

    def solve(self):
        self.downtown_row = {r: list(self.pclues[self.rowclues[r]]) for r in range(self.probsize)}
        self.downtown_col = {c: list(self.pclues[self.colclues[c]]) for c in range(self.probsize)}

        # (1st stage updating) solves all unambigous cases -------------------------
        StrategyCrossSolving.execute(self)

        # (2nd stage updating) solves ambigous cases -----------------------
        after = [len(a[i]) for a in (self.downtown_row, self.downtown_col) for i in range(self.probsize)]
        if after != [1, 1, 1, 1, 1, 1, 1]:
            StrategyStack.execute(self)

        # The kata's result formats differ
        if self.probsize == 7:
            return [list(self.downtown_row[i][0]) for i in range(self.probsize)]
        return tuple(tuple(self.downtown_row[i][0]) for i in range(self.probsize))

