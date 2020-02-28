from itertools import permutations
from collections import deque

# for determinisitic filter only
from collections import Counter

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

    mem = _compute_base_cases(problemsize=4)  # FIXME: HARD CODED problemsize (is a decorator argument)
    mem.update({(0, 0): [set(range(1, 5)) for i in range(4)]})  # corner case, FIXME hard coded range(1,problemsize+1)
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
    # (0) interpreting the cluesindex
    probsize = int(len(clues) / 4)
    colclues, rowclues = _interpret_clues(clues)

    # (1) interterpret cluevalue by lazy compute
    colsets = list(map(_get_cluevalue, colclues))
    rowsets = list(map(_get_cluevalue, rowclues))

    # (2) find already uniquely identified
    # Deprec. be carefull to look columnwise too!
    # downtown = [[rowsets[r][c] & colsets[c][r] for c in range(probsize)] for r in range(probsize)]
    # cnt = Counter()
    # for r, row in enumerate(downtown):
    #     for s in row:
    #         cnt.update(s)
    #     uniques = set([u for u, count in cnt.items() if count == 1])
    #     cnt.clear()
    #
    #     if bool(uniques):  # non empty set, found unique(s)
    #         # get rowwise unique
    #         downtown[r] = [s & uniques if bool(s & uniques) else s for s in row]
    #         for c, s1 in enumerate(downtown[r]):
    #             if len(s1) == 1:
    #                 for colneigb in (*range(0, r), *range(r + 1, 4)):
    #                     downtown[colneigb][c].difference_update(s1)
    #
    # index = list((r, c) for r in range(probsize) for c in range(probsize) if len(downtown[r][c]) > 1)

    # (1) interterpret cluevalue by lazy compute
    colsets = list(map(_get_cluevalue, colclues))
    rowsets = list(map(_get_cluevalue, rowclues))
    downtown = [[rowsets[r][c] & colsets[c][r] for c in range(probsize)] for r in range(probsize)]

    def recurcive_replacement(ind, choice):
        global downtown
        global index
        global stack

        r, c = ind

        # find my non single neighbours ;)
        rowneighb = (tup[1] for tup in index if tup[0] == r and len(downtown[tup[0]][tup[1]]))
        colneighb = (tup[0] for tup in index if tup[1] == c and len(downtown[tup[0]][tup[1]]))

        for r, c in [*rowneighb, *colneighb]:
            repl = downtown[r][c]

            if choice in repl:  # check if the choice need be removed
                downtown[r][c].difference_update({choice})
                stack[choice].append((r, c))

                if not bool(downtown[r][c]):  # empty set after diff: unravel choice
                    return False

                if len(repl) == 2:  # after change there is only one element left
                    recurcive_replacement((r, c), downtown[r][c])
                    index[(r, c)] -= 1

            stack[choice].append(ind)
            index[ind] += 1

    def unravel_choice(stack, ind, choice):
        global index
        index[ind] += 1
        # FIXME: how to reset the choice @ ind position to previous state?
        for r, c in stack:
            downtown[r][c].update(choice)
            index[(r, c)] += 1

    # Deprec: this was the old "sorted" version of index, to get a starter
    # index = list(sorted([(r, c) for r in range(probsize) for c in range(probsize)
    #           if len(downtown[r][c]) != 1], key=lambda tup: len(downtown[tup[0]][tup[1]])))

    #
    index = {(r, c): len(downtown[r][c]) for r in range(probsize) for c in range(probsize)}

    # TODO make temp adaptive to v == 2 if there are no v == 1 ones left.
    #  also: we need only the first element & in each iteration, this version of temp will change!
    #  must compute the next currentpos in each iteration (efficiently!)
    temp = [k for k, v in index.items() if v == 1]
    globstack = []
    currentpos = temp[0]  # starting position
    while set(index.values()) == {1}:   # all indecies have sets of len 1, we succeeded!
        r, c = currentpos
        for choice in downtown[r][c]:
            stack = {k: [] for k in range(1, probsize + 1)}  # for current choice only
            if not bool(recurcive_replacement(index[0], choice)):
                # an empty set occured, choice invalid
                unravel_choice(currentpos, choice, stack)
                continue
            else:  # step succeeded with no empty set # FIXME: no choose the next currentpos
                globstack.append(stack)  # stepwise stack
        # no choice in this step succeeded (since previous decision was faulty)
        # go back one step
        unravel_choice(temp[0], choice, stack=globstack.pop())

    return downtown


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
