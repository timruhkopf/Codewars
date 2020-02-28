from functools import wraps
from itertools import permutations
from collections import deque
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


@timeit
def _sort_permutations(problemsize):
    # sorting the permutations only once by visibility
    permute = list(permutations(list(range(1, problemsize + 1))))
    pclues = {(k, 0): [] for k in range(1, problemsize + 1)}
    for tup in permute:
        ismax = deque([tup[0]])
        for value in tup:
            if ismax[0] < value:
                ismax.appendleft(value)
        pclues[(len(ismax), 0)].append(tup)

    return pclues


@timeit
def _compute_base_cases(problemsize):
    # transpose pclues & get rowsets. Produce baseclues (*,0)
    pclues = _sort_permutations(problemsize)
    for k in pclues.keys():
        pclues[k] = [set(row) for row in zip(*pclues[k])]

    return pclues


def lazycompute(func):
    """lazily compute the cluekeys"""

    @wraps(func)
    def wrapper(cluekey):
        if cluekey in mem.keys():
            return mem[cluekey]
        elif tuple(reversed(cluekey)) in mem.keys():
            mem.update({cluekey: list(reversed(mem[tuple(reversed(cluekey))]))})
        else:
            mem.update(func(cluekey))
        return mem[cluekey]

    mem = _compute_base_cases(problemsize=4)  # FIXME: ONLY HARD CODED problemsize (is a decorator argument)
    return wrapper


@lazycompute
def _get_cluevalue(cluekey):
    """return [cluekey: [set(), set(), set(), set()]} with appropriate sets
    based on cluetuples & the corresponding base cases"""
    return {cluekey: [s0.intersection(s1) for s0, s1 in
                      zip(_get_cluevalue((cluekey[0], 0)), _get_cluevalue((0, cluekey[1])))]}


def _interpret_clues(clues):
    lenc = int(len(clues) / 4)  # for adaptive fieled sizes
    clues = [[clues[j * lenc + i] for i in range(lenc)] for j in range(4)]
    clues = [clue if i in (0, 1) else list(reversed(clue)) for i, clue in enumerate(clues)]

    colclues = [(clues[0][k], clues[0 + 2][k]) for k in range(4)]
    rowclues = [(clues[1 + 2][k], clues[1][k]) for k in range(4)]

    return colclues, rowclues


@timeit
def solve_puzzle(clues):
    problemsize = int(len(clues) / 4)
    colclues, rowclues = _interpret_clues(clues)

    # (3) looking up clues & computing clue values lazily
    colclues = list(map(_get_cluevalue, colclues))
    rowclues = list(map(_get_cluevalue, rowclues))

    # (4) bruteforce with recursion & memoize (Sudoku style)
    downtown = [[rowclues[r][c] & colclues[c][r] for c in range(problemsize)] for r in range(problemsize)]
    matrixindex = list((r, c) for r in range(problemsize) for c in range(problemsize))

    print(downtown)
    print([row for row in zip(*downtown)])  # transpose

    # TODO WE ALREADY SET SOME POSITIONS, AS THERE ARE ROWS,
    #  IN WHICH ONLY A SINGLE SET HOLDS A VALUE - then this set must be
    #  this particular value

    def deterministics(row):
        # fixme make deterministics scalabple for problems
        newrow = list()
        for i, comparand in enumerate(row):
            indexes = tuple(set(range(1, len(row))) - {i})
            temp = comparand - row[indexes[0]].union(*[row[i] for i in indexes[1:]])
            if len(temp) == 0:
                temp = comparand
            newrow.append(temp)

        return newrow

    # deterministics(downtown[3])
    [deterministics(row) for row in downtown]
    map(deterministics, downtown)
    downtown = [deterministics(row) for row in zip(*downtown)]


if __name__ == '__main__':
    # tutorial on how to write unittests
    # https://realpython.com/python-testing/#writing-your-first-test
    import unittest


    class Test_Skyscraper(unittest.TestCase):
        """Tests valid for problemsize = 4"""

        def test_base_case_creation(self):
            mem = _compute_base_cases(problemsize=4)
            self.assertEqual(mem[(2, 0)], [{1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 2, 3, 4}])
            self.assertEqual(mem[(3, 0)], [{1, 2}, {1, 2, 3}, {1, 2, 3, 4}, {1, 2, 3, 4}])

        def test_getcluevalue(self):
            self.assertEqual(_get_cluevalue((2, 0)), [{1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 2, 3, 4}],
                             'Tested, base_case fetch')
            self.assertEqual(_get_cluevalue((1, 3)), [{4}, {1, 2, 3}, {1, 2, 3}, {1, 2}],
                             'Tested creating new values')
            self.assertEqual(_get_cluevalue((3, 1)), list(reversed(_get_cluevalue((1, 3)))),
                             'Tested')
            self.assertEqual(_get_cluevalue((0, 2)), [{1, 2, 3, 4}, {1, 2, 3, 4}, {1, 2, 4}, {1, 2, 3}],
                             'Tested feting flipped base cases')
            self.assertEqual(_get_cluevalue((0, 4)), [{4}, {3}, {2}, {1}],
                             'Tested feting flipped base cases')

        def test_clueparsing(self):
            # FIXME! is the order in rowclues correct? didn't i reverte the rowclues
            self.assertEqual(_interpret_clues(tuple(i for i in range(1, 17)))[0],
                             [(1, 12), (2, 11), (3, 10), (4, 9)], 'Tested colclues')
            self.assertEqual(_interpret_clues(tuple(i for i in range(1, 17)))[1],
                             [(16, 5), (15, 6), (14, 7), (13, 8)], 'Tested colclues')

        def test_preallocate_downtown(self):
            # colclues, rowclues = _interpret_clues(clues)
            # TODO use example from test_clueparsing

            # TODO allocate downtown and check, that no single nested set is empty!

            pass

        def test_pclues(self):
            pclues = _sort_permutations(problemsize=4)
            self.assertEqual(pclues, {(4, 0): [(1, 2, 3, 4)],

                                      (3, 0): [(1, 2, 4, 3),
                                               (1, 3, 2, 4),
                                               (1, 3, 4, 2),
                                               (2, 1, 3, 4),
                                               (2, 3, 1, 4),
                                               (2, 3, 4, 1)],

                                      (2, 0): [(1, 4, 2, 3),
                                               (1, 4, 3, 2),
                                               (2, 1, 4, 3),
                                               (2, 4, 1, 3),
                                               (2, 4, 3, 1),
                                               (3, 1, 2, 4),
                                               (3, 1, 4, 2),
                                               (3, 2, 1, 4),
                                               (3, 2, 4, 1),
                                               (3, 4, 1, 2),
                                               (3, 4, 2, 1)],

                                      (1, 0): [(4, 1, 2, 3),
                                               (4, 1, 3, 2),
                                               (4, 2, 1, 3),
                                               (4, 2, 3, 1),
                                               (4, 3, 1, 2),
                                               (4, 3, 2, 1)]},
                             'Tested sorting of permutations')

        def test_skyscraper4x4(self):
            clues = ((2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3),
                     (0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0))
            outcomes = (((1, 3, 4, 2),
                         (4, 2, 1, 3),
                         (3, 4, 2, 1),
                         (2, 1, 3, 4)),
                        ((2, 1, 4, 3),
                         (3, 4, 1, 2),
                         (4, 2, 3, 1),
                         (1, 3, 2, 4)))
            self.assertEqual(solve_puzzle(clues[0]), outcomes[0])
            self.assertEqual(solve_puzzle(clues[1]), outcomes[1])


    unittest.main()
