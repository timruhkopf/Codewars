from collections import deque
from itertools import permutations

from .Strategies.Strategy2 import Strategy2
from .Strategies.StrategyStack import StrategyStack
from .Util import timeit


class Skyscraper:
    _pclues = {4: None, 6: None, 7: None}  # preallocation to make it work with all

    def __init__(self, clues):
        """
        Solver to
        4*4 Skyscraper: https://www.codewars.com/kata/5671d975d81d6c1c87000022 (kyu 4)
        6*6 Skyscraper: https://www.codewars.com/kata/5679d5a3f2272011d700000d (kyu 2)
        7*7 Skyscraper: https://www.codewars.com/kata/5917a2205ffc30ec3a0000a8 (kyu 1)
        """
        self.clues = clues
        self.probsize = None  # TODO infer probsize

        # parse the clues
        colclues, rowclues = self._interpret_clues(self.clues, self.probsize)
        self.colclues = colclues
        self.rowclues = rowclues

    def __repr__(self):
        # TODO write a debug method, that displays what the current board looks like
        # does this even make sense? since this is a more combinatorical solver.
        pass

    @property
    def pclues(self):
        """property getter ensures, that only when needed, the permutations are ONCE! calculated
        for all problems of the same size,
        :returns dict. describes the visibility of all possible permutations"""
        # TODO check, that the Skyscraper instances do not change the permutations,
        #  but rather they change their copy of it
        if self._pclues[self.probsize] is None:
            self._pclues[self.probsize] = self._sort_permutations(self.probsize)
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
        # TODO testing
        (1,2,3,4) --> 4
        (3,2,1,4) --> 2
        """
        ismax = deque([tup[0]])
        for value in tup:
            if ismax[0] < value:
                ismax.appendleft(value)
        return len(ismax)

    @timeit
    @staticmethod
    def _sort_permutations(problemsize):
        """sorting the permutations by visibility in both directions, creates a lookup table
        for the clues.
        :returns dict.key: visibility from left & right, value: set of """
        permute = set(permutations(range(1, problemsize + 1)))

        # due to lexicographic ordering in permuations: cut no of permutations to half
        # permute = [p for p in permutations(range(1,problemsize +1)) if p[0] < p[-1]]
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

    # @mem_visability(probsize=6)
    # TODO mem_visability decorator???
    def solve(self):
        self.downtown_row = {r: list(self.pclues[self.rowclues[r]]) for r in range(self.probsize)}
        self.downtown_col = {c: list(self.pclues[self.colclues[c]]) for c in range(self.probsize)}

        # (1st stage updating) solves all unambigous cases -------------------------
        Strategy2.execute(self)

        # (2nd stage updating) solves ambigous cases -----------------------
        after = [len(a[i]) for a in (self.downtown_row, self.downtown_col) for i in range(self.probsize)]
        if after != [1, 1, 1, 1, 1, 1, 1]:
            StrategyStack.update_2ndstage(row=0)

        # The kata's result formats differ
        if self.probsize == 7:
            return [list(self.downtown_row[i][0]) for i in range(self.probsize)]
        return tuple(tuple(self.downtown_row[i][0]) for i in range(self.probsize))
