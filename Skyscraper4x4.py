from itertools import permutations
from collections import deque

# auxilary for beautifications
from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def wrapper(*arg, **kwargs):
        t0 = time.time()
        value = func(*arg, **kwargs)
        t1 = time.time()
        print('{} required {} seconds'.format(func.__name__, (t1 - t0)))
        return value

    return wrapper


def visible(tup):
    # ismax = deque(tup.__next__()) # if tup were a generator such as reversed
    ismax = deque([tup[0]])
    for value in tup:
        if ismax[0] < value:
            ismax.appendleft(value)
    return len(ismax)


@timeit
def _sort_permutations(problemsize):
    # sorting the permutations only once by visibility
    permute = permutations(list(range(1, problemsize + 1)))
    pclues = {(k0, k1): [] for k0 in range(1, problemsize + 1) for k1 in range(1, problemsize + 1)}
    # FIXME: this must be changed to accomodate all key combinations (in naive crossprod, there will be keys that cannot reasonably exist !

    for tup in permute:
        fward = visible(tup)
        bward = visible(tup[::-1])

        pclues[(fward, bward)].append(tup)
    return pclues  # FIXME: look here for inapplicable tuples! # also douobles: (2,3) (3,2) the amount stored could be halved!


def _interpret_clues(clues, probsize):
    lenc = int(len(clues) / 4)  # for adaptive fieled sizes
    clues = [[clues[j * lenc + i] for i in range(lenc)] for j in range(4)]
    clues = [clue if i in (0, 1) else list(reversed(clue)) for i, clue in enumerate(clues)]

    colclues = [(clues[0][k], clues[0 + 2][k]) for k in range(probsize)]
    rowclues = [(clues[1 + 2][k], clues[1][k]) for k in range(probsize)]

    return colclues, rowclues


@timeit
def solve_puzzle(clues):
    # (0) interpreting the cluesindex
    probsize = int(len(clues) / 4)
    colclues, rowclues = _interpret_clues(clues, probsize)
    pclues = _sort_permutations(problemsize=4)
    # fixme! must go to solve_puzzle closure to be executed only once.
    #  closure may prevent downtown_row & col to access it though

    # FIXME: be carefull with 0  & (0,0) cases! (are supersets of the lists!)
    #  (0,0) is particularly waseful and should be ignored for the most part!
    # Consider instead, after all list tuple updates are completed, change logic to sets?
    downtown_row = {r: pclues[rowclues[r]] for r in range(probsize)}
    downtown_col = {c: pclues[colclues[c]] for c in range(probsize)}

    @timeit
    def _compute_column_intersect(ind, fix, margin):
        """given a clue, derive at an index position which values are applicable"""
        # transpose pclues & get rowsets.
        if margin == 1:
            fixed = set(col[fix] for col in downtown_col[ind])
        else:
            fixed = set(row[fix] for row in downtown_row[ind])
        return fixed

    # @timeit
    # def _compute_tuple_base(problemsize):
    #     """given a clue, derive all applicable values at each position"""
    #     # transpose pclues & get rowsets. Produce baseclues (*,0)
    #     for k in pclues.keys():
    #         pclues[k] = [set(column) for column in zip(*pclues[k])]
    #
    #     return pclues

    def deselect(fix, choices, margin):
        if margin == 1:
            for tup in downtown_row[fix]:
                if tup[fix] not in choices:
                    downtown_row[fix].remove(tup)

        else:
            for tup in downtown_col[fix]:
                if tup[fix] not in choices:
                    downtown_col[fix].remove(tup)

    # a row update (starting at column 2, updating row 3
    # Consider, that a complexity measure of choices is found in the length of the lists in both downtown dicts
    col_choice = 2
    applicable = _compute_column_intersect(ind=col_choice, fix=3, margin=1)
    deselect(fix=3, choices=applicable, margin=1)



    # (4) convert to required format
    # return tuple(tuple(int(*downtown[(r, c)]) for c in range(probsize)) for r in range(probsize))


if __name__ == '__main__':
    # # tutorial on how to write unittests
    # # https://realpython.com/python-testing/#writing-your-first-test
    import unittest


    class Test_Skyscraper(unittest.TestCase):

        def test_clueparsing(self):
            self.assertEqual(_interpret_clues(tuple(i for i in range(1, 17)))[0],
                             [(1, 12), (2, 11), (3, 10), (4, 9)], 'Tested colclues')
            self.assertEqual(_interpret_clues(tuple(i for i in range(1, 17)))[1],
                             [(16, 5), (15, 6), (14, 7), (13, 8)], 'Tested colclues')

        # def test_pclues(self):
        #     pclues = _sort_permutations(problemsize=4)
        # self.assertEqual(pclues, {(4, 0): [(1, 2, 3, 4)],
        #
        #                           (3, 0): [(1, 2, 4, 3),
        #                                    (1, 3, 2, 4),
        #                                    (1, 3, 4, 2),
        #                                    (2, 1, 3, 4),
        #                                    (2, 3, 1, 4),
        #                                    (2, 3, 4, 1)],
        #
        #                           (2, 0): [(1, 4, 2, 3),
        #                                    (1, 4, 3, 2),
        #                                    (2, 1, 4, 3),
        #                                    (2, 4, 1, 3),
        #                                    (2, 4, 3, 1),
        #                                    (3, 1, 2, 4),
        #                                    (3, 1, 4, 2),
        #                                    (3, 2, 1, 4),
        #                                    (3, 2, 4, 1),
        #                                    (3, 4, 1, 2),
        #                                    (3, 4, 2, 1)],
        #
        #                           (1, 0): [(4, 1, 2, 3),
        #                                    (4, 1, 3, 2),
        #                                    (4, 2, 1, 3),
        #                                    (4, 2, 3, 1),
        #                                    (4, 3, 1, 2),
        #                                    (4, 3, 2, 1)]},
        #                  'Tested sorting of permutations')

        def test_skyscraper4x4(self):
            clues = ((2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3),
                     (0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0),
                     [1, 2, 4, 2, 2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1],
                     [2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2])

            outcomes = (((1, 3, 4, 2),
                         (4, 2, 1, 3),
                         (3, 4, 2, 1),
                         (2, 1, 3, 4)),

                        ((2, 1, 4, 3),
                         (3, 4, 1, 2),
                         (4, 2, 3, 1),
                         (1, 3, 2, 4)),

                        ((4, 2, 1, 3),  # FIXME: this one has multiple time same value in a row!
                         (3, 1, 2, 4),
                         (1, 4, 3, 2),
                         (2, 3, 4, 1)),

                        ((3, 4, 2, 1),
                         (1, 2, 3, 4),
                         (2, 1, 4, 3),
                         (4, 3, 1, 2)))

            self.assertEqual(solve_puzzle(clues[0]), outcomes[0])
            self.assertEqual(solve_puzzle(clues[1]), outcomes[1])
            self.assertEqual(solve_puzzle(clues[2]), outcomes[2])


    unittest.main()

    # d = solve_puzzle((0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0))

# print(d)
