"""
4*4 Skyscraper: https://www.codewars.com/kata/5671d975d81d6c1c87000022
6*6 Skyscraper: https://www.codewars.com/kata/5679d5a3f2272011d700000d
7*7 Skyscraper: https://www.codewars.com/kata/5917a2205ffc30ec3a0000a8
"""

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
    pclues.update({(0, 0): permute})
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

    downtown_row = {r: list(pclues[rowclues[r]]) for r in range(probsize)}
    downtown_col = {c: list(pclues[colclues[c]]) for c in range(probsize)}

    def update(col, margin=1):
        """column update for margin== 1, rowupdate if margin == 0"""

        pos1 = (downtown_row, downtown_col)[margin]
        pos2 = (downtown_row, downtown_col)[margin - 1]

        # updating rows indepenendly based on column
        fix = [set(column) for column in zip(*pos1[col])]
        for i, valid in enumerate(fix):
            pos2[i] = [tup for tup in pos2[i] if tup[col] in valid]

        _update_det(pos1, fix, col)

    def _update_det(pos1, fix, col):
        """update deterministics across "columns" & early stopping!"""
        uniques = list((i, v) for i, v in enumerate(fix) if len(v) == 1)
        stack = {k: [] for k in range(probsize)}
        for j in {*range(probsize)} - {col}:
            for tup in pos1[j]:
                for i, v in uniques:
                    if tup[i] in v:
                        pos1[j].remove(tup)
                        stack[j].append(tup)
                        break
        return stack  # relevant only for last 7*7er case

    def update_2ndstage(row):
        """recursive solving for the last remaining ambigous case"""
        for choice in downtown_row[row]:
            stack = _update_det(pos1=downtown_row, fix=[set([v]) for v in choice], col=row)
            downtown_row[row] = [choice]

            after = [len(row) for row in downtown_row.values()]
            if not all(after):
                _revert(stack)
                continue

            elif row != probsize - 1:  # there are more rows
                if update_2ndstage(row + 1):
                    return True
                else:
                    continue

            elif after == [1, 1, 1, 1, 1, 1, 1]:
                return True

        if after != [1, 1, 1, 1, 1, 1, 1]:  # all choices faulty
            _revert(stack)
            return False

    def _revert(stack):
        for k, v in stack.items():
            downtown_row[k].extend(v)

    # (1st stage updating) solves all unambigous cases -------------------------
    before = []
    after = [len(a[i]) for a in (downtown_row, downtown_col) for i in range(probsize)]
    while before != after:
        before = after
        for row in sorted(range(probsize), key=lambda i: len(downtown_row[i])):
            update(row, margin=0)

        for col in sorted(range(probsize), key=lambda i: len(downtown_col[i])):
            update(col, margin=1)

        after = [len(a[i]) for a in (downtown_row, downtown_col) for i in range(probsize)]

    # (2nd stage updating) solves ambigous cases -----------------------
    if after != [1, 1, 1, 1, 1, 1, 1]:
        update_2ndstage(row=0)

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

        # def test_skyscraper4x4(self):
        #     self.assertEqual(solve_puzzle((2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3)), \
        #                      ((1, 3, 4, 2),
        #                       (4, 2, 1, 3),
        #                       (3, 4, 2, 1),
        #                       (2, 1, 3, 4)))
        #
        #     self.assertEqual(solve_puzzle((0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0)), \
        #                      ((2, 1, 4, 3),
        #                       (3, 4, 1, 2),
        #                       (4, 2, 3, 1),
        #                       (1, 3, 2, 4)))
        #
        #     self.assertEqual(solve_puzzle([1, 2, 4, 2, 2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1]), \
        #                      ((4, 2, 1, 3),
        #                       (3, 1, 2, 4),
        #                       (1, 4, 3, 2),
        #                       (2, 3, 4, 1)))
        #
        #     self.assertEqual(solve_puzzle([2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]), \
        #                      ((3, 4, 2, 1),
        #                       (1, 2, 3, 4),
        #                       (2, 1, 4, 3),
        #                       (4, 3, 1, 2)))

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
