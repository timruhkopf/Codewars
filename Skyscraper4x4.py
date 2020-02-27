from itertools import permutations
from collections import deque

problemsize = 4


def _sort_permutations():
    # sorting the permutations only once by visibility
    permute = list(permutations(list(range(1, problemsize + 1))))
    pclues = {k: [] for k in range(1, problemsize + 1)}
    for tup in permute:
        ismax = deque([tup[0]])
        for value in tup:
            if ismax[0] < value:
                ismax.appendleft(value)
        pclues[len(ismax)].append(tup)

    return pclues

def _compute_base_cases():
    pclues = _sort_permutations()

    # compute base cases (*,0)
    mem = {(k, 0): [set(), set(), set(), set()] for k in range(1, problemsize + 1)}
    for k, lclues in pclues.items():
        for clue in lclues:
            for i, value in enumerate(clue):
                mem[(k, 0)][i].update([value])

    # compute base cases (0,*)
    for k in list(mem.keys()):
        mem.update({tuple(reversed(k)): list(reversed(mem[k]))})

    return mem


mem = _compute_base_cases()
def lazycompute(func):
    """lazily compute the cluekeys"""

    def wrapper(cluekey):
        if cluekey in mem.keys():
            return mem[cluekey]
        elif tuple(reversed(cluekey)) in mem.keys():
            mem.update({cluekey: list(reversed(mem[tuple(reversed(cluekey))]))})
        else:
            mem.update(func(cluekey))
        return mem[cluekey]

    return wrapper


@lazycompute
def _get_cluevalue(cluekey):
    """return [cluekey: [set(), set(), set(), set()]} with appropriate sets
    based on cluetuples & the corresponding base cases"""
    return {cluekey: [s0.intersection(s1) for s0, s1 in
                      zip(mem[(cluekey[0], 0)], mem[(cluekey[1], 0)])]}


def _interpret_clues(clues):
    # (2) clue parsing: getting row- & columnclues
    lenc = int(len(clues) / 4)  # for adaptive fieled sizes
    clues = [[clues[j * lenc + i] for i in range(lenc)] for j in range(4)]
    clues = [clue if i % 2 == 0 else list(reversed(clue)) for i, clue in enumerate(clues)]

    colclues = [(clues[0][k], clues[0 + 2][k]) for k in range(4)]
    rowclues = [(clues[1 + 2][k], clues[1][k]) for k in range(4)]

    return colclues, rowclues


def _preallocate_downtown(colclues, rowclues):
    matrixindex = list((r, c) for r in range(problemsize) for c in range(problemsize))
    downtown = list(list(0 for i in range(4)) for j in range(problemsize))
    for (r, c) in matrixindex:
        # downtown[r][c] = rowclues[r][c] & colclues[c][r]
        print((r, c), rowclues[r], colclues[c], rowclues[r][c], colclues[c][r], rowclues[r][c] & colclues[c][r])
        # print((r, c), get_cluevalue(colclues1[c]), get_cluevalue(rowclues1[r]))

    return downtown, matrixindex


def solve_puzzle(clues):
    colclues, rowclues = _interpret_clues(clues)

    # (3) looking up clues & computing clue values lazily
    colclues = list(map(_get_cluevalue, colclues))
    rowclues = list(map(_get_cluevalue, rowclues))

    # (4) bruteforce with recursion & memoize (Sudoku style)
    downtown, matrixindex = _preallocate_downtown(colclues, rowclues)


if __name__ == '__main__':
    # tutorial on how to write unittests
    # https://realpython.com/python-testing/#writing-your-first-test
    import unittest


    class Test_Skyscraper(unittest.TestCase):
        """Tests valid for problemsize = 4"""

        def test_base_case_creation(self):
            mem = _compute_base_cases()
            self.assertEqual(mem[(2, 0)], {(2, 0): [{1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 2, 3, 4}]})
            self.assertEqual(mem[(0, 2)], {(0, 2): [{1, 2, 3, 4}, {1, 2, 3, 4}, {1, 2, 4}, {1, 2, 3}]})
            self.assertEqual(mem[(3, 0)], {(3, 0): [{1, 2}, {1, 2, 3}, {1, 2, 3, 4}, {1, 2, 3, 4}]})
            self.assertEqual(mem[(0, 4)], {(0, 4): [{4}, {3}, {2}, {1}]})

        def test_getcluevalue(self):
            self.assertEqual(_get_cluevalue((2, 0)), {(2, 0): [{1, 2, 3}, {1, 2, 4}, {1, 2, 3, 4}, {1, 2, 3, 4}]},
                             'Tested, base_case fetch')
            self.assertEqual(_get_cluevalue(1, 3), {(1, 3): [{4}, {1, 2, 3, 4}, {1, 2, 3}, {1, 2}]},
                             'Tested creating new values')
            self.assertEqual(_get_cluevalue((3, 1), _get_cluevalue(1, 3)),
                             'Tested')

        def test_clueparsing(self):
            colclues = ((1, 12), (2, 11), (3, 10), (4, 9))
            # FIXME! is the order in rowclues correct? didn't i reverte the rowclues
            rowclues = ((5, 16), (6, 15), (7, 14), (8, 13))
            self.assertEqual(_interpret_clues(tuple(i for i in range(1, 17))),
                             (colclues, rowclues), 'Tested clueparsing')

        def test_preallocate_downtown(self):
            # colclues, rowclues = _interpret_clues(clues)
            # TODO use example from test_clueparsing

            # TODO allocate downtown and check, that no single nested set is empty!

            pass

        def test_pclues(self):
            pclues = _sort_permutations()
            self.assertEqual(pclues, {4: [(1, 2, 3, 4)],

                                      3: [(1, 2, 4, 3),
                                          (1, 3, 2, 4),
                                          (1, 3, 4, 2),
                                          (2, 1, 3, 4),
                                          (2, 3, 1, 4),
                                          (2, 3, 4, 1)],

                                      2: [(1, 4, 2, 3),
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

                                      1: [(4, 1, 2, 3),
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
