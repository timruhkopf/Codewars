from itertools import permutations
from collections import deque

problemsize = 4


def lazycompute(func):
    """lazily compute the cluekeys"""

    def wrapper(cluekey):
        if cluekey in mem.keys():
            return mem[cluekey]
        elif tuple(reversed(cluekey)) in mem.keys():
            mem.update({cluekey: list(reversed(mem[tuple(reversed(cluekey))]))})
        else:
            mem.update(func(cluekey, basemem))
        return mem[cluekey]

    # EXECUTE THE FOLLOWING ONLY ONCE

    # sorting the permutations only once by visability
    permute = list(permutations(list(range(1, problemsize + 1))))
    pclues = {k: [] for k in range(1, problemsize + 1)}
    for tup in permute:
        ismax = deque([tup[0]])
        for value in tup:
            if ismax[0] < value:
                ismax.appendleft(value)
        pclues[len(ismax)].append(tup)

    # compute base cases (*,0)
    mem = {(k, 0): [set(), set(), set(), set()] for k in range(1, problemsize + 1)}
    for k, lclues in pclues.items():
        for clue in lclues:
            for i, value in enumerate(clue):
                mem[(k, 0)][i].update([value])

    # compute base cases (0,*)
    for k in list(mem.keys()):
        mem.update({tuple(reversed(k)): list(reversed(mem[k]))})

    basemem = mem.copy()

    return wrapper


@lazycompute
def get_cluevalue(cluekey, basedict):
    # FIXME do not pass basedict as it is copied in every lookup. instead access memmoized dict immediately!
    """return [cluekey: [set(), set(), set(), set()]} with appropriate sets based on pclues"""
    return {cluekey: [s0.intersection(s1) for s0, s1 in
                      zip(basedict[(cluekey[0], 0)], basedict[(cluekey[1], 0)])]}


def solve_puzzle(clues):
    # (2) clue parsing: getting row- & columnclues
    lenc = int(len(clues) / 4)  # for adaptive fieled sizes
    clues = [[clues[j * lenc + i] for i in range(lenc)] for j in range(4)]
    clues = [clue if i % 2 == 0 else list(reversed(clue)) for i, clue in enumerate(clues)]

    # columnclues, rowclues = [[(clues[i][k], clues[i + 2][k]) for k in range(4)] for i in [0, 1]]
    colclues1 = [(clues[0][k], clues[0 + 2][k]) for k in range(4)]
    rowclues1 = [(clues[1 + 2][k], clues[1][k]) for k in range(4)]

    # (3) looking up clues & computing clue values lazily
    colclues = list(map(get_cluevalue, colclues1))
    rowclues = list(map(get_cluevalue, rowclues1))

    # (4) bruteforce with recursion & memoize (Sudoku style)
    matrixindex = list((r, c) for r in range(problemsize) for c in range(problemsize))
    downtown = list(list(0 for i in range(4)) for j in range(problemsize))

    for (r, c) in matrixindex:
        # downtown[r][c] = rowclues[r][c] & colclues[c][r]
        print((r, c), rowclues1[r], colclues1[c], rowclues[r][c], colclues[c][r], rowclues[r][c] & colclues[c][r])
        # print((r, c), get_cluevalue(colclues1[c]), get_cluevalue(rowclues1[r]))

    print('')

if __name__ == '__main__':
    # interpret_clues()

    clues = ((2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3),
             (0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0))

    solve_puzzle(clues[0])

    outcomes = (
        ((1, 3, 4, 2),
         (4, 2, 1, 3),
         (3, 4, 2, 1),
         (2, 1, 3, 4)),
        ((2, 1, 4, 3),
         (3, 4, 1, 2),
         (4, 2, 3, 1),
         (1, 3, 2, 4))
    )

    if solve_puzzle(clues[0]) != outcomes[0]:
        raise ValueError

    if solve_puzzle(clues[1]) != outcomes[1]:
        raise ValueError
