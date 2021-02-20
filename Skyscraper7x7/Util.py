import time
from functools import wraps

from Skyscraper7x7.Solver.Solver import Skyscraper


def solve_puzzle(clues):
    """The kata's interface requires a functional interface."""
    return Skyscraper(clues).solve()


def timeit(func):
    @wraps(func)
    def wrapper(*arg, **kwargs):
        t0 = time.time()
        value = func(*arg, **kwargs)
        t1 = time.time()
        print('{} required {} seconds'.format(func.__name__, (t1 - t0)))
        return value

    return wrapper
