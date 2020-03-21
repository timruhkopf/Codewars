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


def _visible(tup):
    # ismax = deque(tup.__next__()) # if tup were a generator such as reversed
    ismax = deque([tup[0]])
    for value in tup:
        if ismax[0] < value:
            ismax.appendleft(value)
    return len(ismax)


@timeit
def _sort_permutations(problemsize):
    """sorting the permutations by visibility"""
    permute = set(permutations(range(1, problemsize + 1)))

    # due to lexicographic ordering in permuations: cut no of permutations to half
    # permute = [p for p in permutations(range(1,problemsize +1)) if p[0] < p[-1]]
    gen = range(1, problemsize + 1)
    pclues = {(k0, k1): set() for k0 in gen for k1 in gen}
    for tup in permute:
        fward = _visible(tup)
        bward = _visible(tup[::-1])

        pclues[(fward, bward)].add(tup)

    pclues.update({(0, k): set.union(*(pclues[(i, k)] for i in gen)) for k in gen})  # supersets
    pclues.update({(k, 0): set.union(*(pclues[(k, i)] for i in gen)) for k in gen})
    pclues = {k: v for k, v in pclues.items() if len(v) != 0}
    pclues.update({(0, 0): permute})  # todo: ignore 0,0 in update process! # set()

    # FIXME: this must be changed to accomodate all key combinations (in naive crossprod, there will be keys that cannot reasonably exist !

    # Deprec: remove me
    # info on how informative each clue is (excluding 0,0)
    for p, v in pclues.items():
        print(p, len(v))

    return pclues


def _interpret_clues(clues, probsize):
    """interpret the clues: returns lists of tuples which indicate the full row & col info"""
    clues = [[clues[j * probsize + i] for i in range(probsize)] for j in range(4)]
    clues = [clue if i in (0, 1) else list(reversed(clue)) for i, clue in enumerate(clues)]

    colclues = [(clues[0][k], clues[0 + 2][k]) for k in range(probsize)]
    rowclues = [(clues[1 + 2][k], clues[1][k]) for k in range(probsize)]

    return colclues, rowclues


def mem_visability(probsize):
    """ensures visability is computed only once for all solve calls"""
    pclues = _sort_permutations(problemsize=probsize)

    def real_decorator(f):
        def wrapper(clue):
            return f(clue, probsize, pclues)

        return wrapper

    return real_decorator


@timeit
@mem_visability(probsize=7)
def solve_puzzle(clues, probsize, pclues):
    colclues, rowclues = _interpret_clues(clues, probsize)

    downtown_row = {r: pclues[rowclues[r]] for r in range(probsize)}
    downtown_col = {c: pclues[colclues[c]] for c in range(probsize)}

    # TODO Remove me!
    for p, v in downtown_row.items():
        print(p, len(v))

    for p, v in downtown_col.items():
        print(p, len(v))

    def _col_update(col):
        # TODO make only one function for both _col & _row_update
        # updating rows indepenendly
        fix = [set(column) for column in zip(*downtown_col[col])]
        for i, valid in enumerate(fix):
            downtown_row[i] = [tup for tup in downtown_row[i] if tup[col] in valid]

        # update deterministics across columns
        for i, val in enumerate(fix):
            if len(val) == 1:
                for j in {*range(probsize)} - {col}:
                    # TODO no refetching and multiple accesses due to i (switch i & j order  & doe only one list comp!
                    downtown_col[j] = [tup for tup in downtown_col[j] if tup[i] not in val]

        # FIXME: make sure, unique updates are carried out only once!!

    def _row_update(row):
        # TODO make only one function for both _col & _row_update
        fix = [set(row1) for row1 in zip(*downtown_row[row])]  # set@index
        for i, valid in enumerate(fix):
            downtown_col[i] = [tup for tup in downtown_col[i] if tup[row] in valid]

        # update deterministics
        for i, val in enumerate(fix):
            if len(val) == 1:
                for j in {*range(probsize)} - {row}:
                    # TODO no refetching and multiple accesses due to i
                    downtown_row[j] = [tup for tup in downtown_row[j] if tup[i] not in val]

    before, after = False, True
    while before != after:
        before = [len(a[i]) for a in (downtown_row, downtown_col) for i in range(probsize)]

        for row in sorted(range(probsize), key=lambda i: len(downtown_row[i])):
            _row_update(row)
        for col in sorted(range(probsize), key=lambda i: len(downtown_col[i])):
            _col_update(col)

        after = [len(a[i]) for a in (downtown_row, downtown_col) for i in range(probsize)]

    # (4) convert to required format

    # TODO remove me
    a = [[set(row1) for row1 in zip(*downtown_row[row])] for row in range(probsize)]
    b = [[set(row1) for row1 in zip(*downtown_col[row])] for row in range(probsize)]
    a = tuple(tuple(a[i]) for i in range(probsize))
    b = tuple(tuple(b[i]) for i in range(probsize))

    # TODO begining of a brute force approach
    # choice = downtown_col[0][1]  # col = 0
    # col = 0
    # for i, valid in enumerate(choice):
    #     downtown_row[i] = [tup for tup in downtown_row[i] if tup[col] == valid]

    if probsize == 7:
        return [list(downtown_row[i][0]) for i in range(probsize)]
    return tuple(tuple(downtown_row[i][0]) for i in range(probsize))


if __name__ == '__main__':
    # # tutorial on how to write unittests
    # # https://realpython.com/python-testing/#writing-your-first-test
    import unittest


    class Test_Skyscraper(unittest.TestCase):
        # TODO test permutations & visibility

        def test_clueparsing(self):
            self.assertEqual(_interpret_clues(tuple(i for i in range(1, 17)), probsize=4)[0],
                             [(1, 12), (2, 11), (3, 10), (4, 9)], 'Tested colclues')
            self.assertEqual(_interpret_clues(tuple(i for i in range(1, 17)), probsize=4)[1],
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

        # def test_skyscraper4x4(self):
        #     clues = ((2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3),
        #              (0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0),
        #              [1, 2, 4, 2, 2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1],
        #              [2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2])
        #
        #     outcomes = (((1, 3, 4, 2),
        #                  (4, 2, 1, 3),
        #                  (3, 4, 2, 1),
        #                  (2, 1, 3, 4)),
        #
        #                 ((2, 1, 4, 3),
        #                  (3, 4, 1, 2),
        #                  (4, 2, 3, 1),
        #                  (1, 3, 2, 4)),
        #
        #                 ((4, 2, 1, 3),
        #                  (3, 1, 2, 4),
        #                  (1, 4, 3, 2),
        #                  (2, 3, 4, 1)),
        #
        #                 ((3, 4, 2, 1),
        #                  (1, 2, 3, 4),
        #                  (2, 1, 4, 3),
        #                  (4, 3, 1, 2)))
        #
        #     self.assertEqual(solve_puzzle(clues[0]), outcomes[0])
        #     # self.assertEqual(solve_puzzle(clues[1]), outcomes[1])
        #     self.assertEqual(solve_puzzle(clues[2]), outcomes[2])
        #     self.assertEqual(solve_puzzle(clues[3]), outcomes[3])

        # def test_skyscraper6x6(self):
        #     self.assertEqual(
        #         solve_puzzle((0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0)),
        #         ((5, 6, 1, 4, 3, 2),
        #          (4, 1, 3, 2, 6, 5),
        #          (2, 3, 6, 1, 5, 4),
        #          (6, 5, 4, 3, 2, 1),
        #          (1, 2, 5, 6, 4, 3),
        #          (3, 4, 2, 5, 1, 6)))
        #
        #     self.assertEqual(
        #         solve_puzzle((3, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2, 5, 1, 2, 2, 4, 3, 3, 2, 1, 2, 2, 4)),
        #         ((2, 1, 4, 3, 5, 6),
        #          (1, 6, 3, 2, 4, 5),
        #          (4, 3, 6, 5, 1, 2),
        #          (6, 5, 2, 1, 3, 4),
        #          (5, 4, 1, 6, 2, 3),
        #          (3, 2, 5, 4, 6, 1)))
        #
        #     self.assertEqual(
        #         solve_puzzle((0, 3, 0, 5, 3, 4, 0, 0, 0, 0, 0, 1, 0, 3, 0, 3, 2, 3, 3, 2, 0, 3, 1, 0)),
        #         ((5, 2, 6, 1, 4, 3),
        #          (6, 4, 3, 2, 5, 1),
        #          (3, 1, 5, 4, 6, 2),
        #          (2, 6, 1, 5, 3, 4),
        #          (4, 3, 2, 6, 1, 5),
        #          (1, 5, 4, 3, 2, 6)))

        def test_skyscraper7x7(self):
            self.assertEqual(
                solve_puzzle([3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3]), \
                [[2, 1, 4, 7, 6, 5, 3],
                 [6, 4, 7, 3, 5, 1, 2],
                 [1, 2, 3, 6, 4, 7, 5],
                 [5, 7, 6, 2, 3, 4, 1],
                 [4, 3, 5, 1, 2, 6, 7],
                 [7, 6, 2, 5, 1, 3, 4],
                 [3, 5, 1, 4, 7, 2, 6]])


    unittest.main()

# print(d)
