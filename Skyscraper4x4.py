from itertools import permutations, combinations
from collections import deque


def interpret_clues():
    # (1) sort the possible permutations for each clue
    #     All of (1.) can be computed only once for all cases yet to come.
    #     Consider writing it in a seperate function & do memoize

    # a) Use deque comparisons (am i greater than you, i stay comperand,
    #    if not, you are new comperand & increase counter. Number of switches is
    #    directly related with tip

    # b) Lookup the max value's index position (as this is the max tip number
    #    that can still be achieved and proceed with a).



    # # possible combinations (sanity check for 4x4)
    # pclues1 = {4: [(1, 2, 3, 4)],
    #
    #           3: [(1, 2, 4, 3),
    #               (1, 3, 2, 4),
    #               (1, 3, 4, 2),
    #               (2, 1, 3, 4),
    #               (2, 3, 1, 4),
    #               (2, 3, 4, 1)],
    #
    #           2: [(1, 4, 2, 3),
    #               (1, 4, 3, 2),
    #               (2, 1, 4, 3),
    #               (2, 4, 1, 3),
    #               (2, 4, 3, 1),
    #               (3, 1, 2, 4),
    #               (3, 1, 4, 2),
    #               (3, 2, 1, 4),
    #               (3, 2, 4, 1),
    #               (3, 4, 1, 2),
    #               (3, 4, 2, 1)],
    #
    #           1: [(4, 1, 2, 3),
    #               (4, 1, 3, 2),
    #               (4, 2, 1, 3),
    #               (4, 2, 3, 1),
    #               (4, 3, 1, 2),
    #               (4, 3, 2, 1)]}

    # (1) sort permutations by no. of visible skyscapers
    permute = list(permutations([1, 2, 3, 4]))
    pclues = {k: [] for k in range(1, 5)}
    for tup in permute:
        ismax = deque(tup[0])
        for value in tup:
            if ismax[0] < value:
                ismax.appendleft(value)
        pclues[len(ismax)].append(tup)  # counter of comparisons is len()

    # (1.2) for each clue, get the indexposition set
    dclues = {(k, 0): [set(), set(), set(), set()] for k in range(1, 5)}
    for k, lclues in pclues.items():
        for clue in lclues:
            for i, value in enumerate(clue):
                dclues[(k, 0)][i].update([value])

    # (1.3) get unique clues (that can be reverted)
    # dclues already shows: some combinations are invalid! (empty sets)
    unique_info_sets = list(combinations([1, 2, 3, 4], r=2))
    dclues.update({(k0, k1): [] for k0, k1 in unique_info_sets})
    for k0, k1 in unique_info_sets:
        for s0, s1 in zip(dclues[(k0, 0)], reversed(dclues[(k1, 0)])):
            dclues[(k0, k1)].append(s0.intersection(s1))


def solve_puzzle(clues):
    # (2) clue parsing: getting row- & columnclues
    lenc = int(len(clues) / 4)  # for adaptive fieled sizes
    clues = [[clues[j * lenc + i] for i in range(lenc)] for j in range(4)]
    clues = [clue if i % 2 == 0 else list(reversed(clue)) for i, clue in enumerate(clues)]
    columnclues, rowclues = [[(clues[i][k], clues[i + 2][k]) for k in range(4)] for i in [0, 1]]

    # (3) looking up clues & filling them into the solution space
    # Todo make dclues avaliable for lookup!
    for clue in columnclues:
        if clue == sorted(clue):
            dclues[clue]
        else:
            # ToDo a call on dclues with a yet not comuted (reversed tupel)
            #  should calculate the reversed clue & add it to dclues, to ease
            #  later lookups.
            dclues[tuple(reversed(clue))]

    # (4) bruteforce with recursion & memoize (Sudoku style)


if __name__ == '__main__':
    interpret_clues()

    clues = ((2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3),
             (0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0))

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
