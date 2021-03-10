import types
from collections import deque


def delta(values, n):
    if not isinstance(values, types.GeneratorType):
        values = iter(values)

    # setup
    d = {0: list(next(values) for i in range(n))}  # prefill the first n values
    for level in range(1, n + 1):
        d[level] = [first - second for first, second in zip(list(d[level - 1])[1:], d[level - 1])]

        # to save memory, remove all but the last two values
        d[level - 1] = deque(d[level - 1][-2:], maxlen=2)

    d[n] = deque(d[n][-2:], maxlen=2)

    while True:
        try:
            d[0].append(next(values))
            for level in sorted(k for k in d.keys() if k > 0):
                d[level].append(d[level - 1][-1] - d[level - 1][-2])

            yield d[n][-1]
        except StopIteration:
            break



def delta(values, n):
    values = iter(values) if n==1 else delta(values, n-1)
    a = next(values)
    for b in values:
        yield b - a
        a = b



