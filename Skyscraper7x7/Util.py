import time
from functools import wraps

from .Solver import Skyscraper


def timeit(func):
    @wraps(func)
    def wrapper(*arg, **kwargs):
        t0 = time.time()
        value = func(*arg, **kwargs)
        t1 = time.time()
        print('{} required {} seconds'.format(func.__name__, (t1 - t0)))
        return value

    return wrapper


def solve_puzzle(clues):
    return Skyscraper(clues).solve()
