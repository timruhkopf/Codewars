from itertools import permutations, combinations
from collections import deque


# (1) sort the possible permutations for each clue
#     All of (1.) can be computed only once for all cases yet to come.
#     Consider writing it in a seperate function & do memoize

# (1) sort permutations by no. of visible skyscapers
# a) Use deque comparisons (am i greater than you, i stay comperand,
#    if not, you are new comperand & increase counter. Number of switches is
#    directly related with tip
# [ b) Lookup the max value's index position (as this is the max tip number
#    that can still be achieved and proceed with a).]
# counter of comparisons is len()

def memoize(func):
    """lazily compute the cluekeys"""
    # sorting the permutations only once by visability
    permute = list(permutations([1, 2, 3, 4]))
    pclues = {k: [] for k in range(1, 5)}
    for tup in permute:
        ismax = deque([tup[0]])
        for value in tup:
            if ismax[0] < value:
                ismax.appendleft(value)
        pclues[len(ismax)].append(tup)

    # compute base cases (*,0)
    func.mem = {(k, 0): [set(), set(), set(), set()] for k in range(1, 5)}
    for k, lclues in pclues.items():
        for clue in lclues:
            for i, value in enumerate(clue):
                func.mem[(k, 0)][i].update([value])

    def wrapper(cluekey):
        if cluekey in func.mem.keys():
            return func.mem[cluekey]
        elif tuple(reversed(cluekey)) in func.mem.keys():
            func.mem[cluekey].update(tuple(reversed(func.mem[tuple(reversed(cluekey))])))
        else:
            func.mem.update(func(cluekey))

        return func.mem[cluekey]

    return wrapper

def recmemo(f):
    def helper(position, counter):
        helper.calls += 1
        helper.memo[position] = f(position, counter)
        return helper.memo[position]

    helper.calls = 0
    helper.memo = {}
    return helper

# def get_baseclue(cluekey):
#     # (1.2) for each clue, get the indexposition set
#     sets = [set(), set(), set(), set()]
#     for clue in get_cluevalue.pclues[cluekey[cluekey != 0]]:
#         for i, value in enumerate(clue):
#             sets[i].update([value])
#     return {cluekey: sets}
#


@memoize
def get_cluevalue(cluekey):
    """return [cluekey: [set(), set(), set(), set()]} with appropriate sets based on pclues"""
    return {cluekey: [s0.intersection(s1) for s0, s1 in zip(get_cluevalue.mem[(cluekey[0], 0)],
                      reversed(get_cluevalue.mem[(cluekey[1], 0)]))]}


def solve_puzzle(clues):
    # (2) clue parsing: getting row- & columnclues
    lenc = int(len(clues) / 4)  # for adaptive fieled sizes
    clues = [[clues[j * lenc + i] for i in range(lenc)] for j in range(4)]
    clues = [clue if i % 2 == 0 else list(reversed(clue)) for i, clue in enumerate(clues)]

    # columnclues, rowclues = [[(clues[i][k], clues[i + 2][k]) for k in range(4)] for i in [0, 1]]
    colclues = [(clues[0][k], clues[0 + 2][k]) for k in range(4)]
    rowclues = [(clues[1 + 2][k], clues[1][k]) for k in range(4)]

    # (3) looking up clues & computing clue values lazily
    colclues = list(map(get_cluevalue, colclues))
    rowclues = list(map(get_cluevalue, rowclues))

    # (4) bruteforce with recursion & memoize (Sudoku style)
    matrixindex = list((r, c) for r in range(4) for c in range(4))

    @recmemo
    def solv(position, counter):
        '''recursive path trough the problem, whilst considering only applicable paths'''
        r, c = position
        S = rowclues[r] & colclues[c]
        for s in S:
            if counter + 1 == len(matrixindex):  # base case: last zero value is reached
                return s
            else:  # go further down on path with current s
                rowclues[r].difference_update({s})
                colclues[c].difference_update({s})
                sol = solv(matrixindex[counter + 1], counter + 1)

                if bool(sol):  # the next step returned a non empty solution
                    return s
                else:  # the next zero index returns {}
                    # i.e. it has no applicable choices: Go up
                    # add s to sets it was removed from
                    rowclues[r].update({s})
                    colclues[c].update({s})
                    continue
        return {}

    solv(position=matrixindex[0], counter=0)
    # print(solv.memo)

    for (r, c), val in solv.memo.items():
        downtown[r][c] = val



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
