import time
from collections import deque
# auxiliary imports for beautifications
from functools import wraps
from itertools import permutations


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
