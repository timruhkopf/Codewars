# import types

from collections import deque


# def delta(values, n):
#     if isinstance(values, types.GeneratorType):
#         a = next(values)
#         while True:
#             b = next(values)
#             yield b - a
#             a = b
#     else:
#         ret = values.copy()
#         for i in range(n):
#             ret = [i[1] - i[0] for i in zip(ret, ret[1::])]
#         return ret


def delta(values, n):
    # setup
    d = {level: deque([], maxlen=length) for level, length in zip(range(n), reversed(range(n + 1)))}
    d[0].extend(values[0:n])  # prefill the first n values

    for level in sorted(k for k in d.keys() if k != 0):
        d[level].extend(first - second for first, second in zip(list(d[level - 1])[1:], d[level - 1]))

    yield d[n - 1][-1]

    iterator = iter(values[n:])
    while True:
        d[0].append(next(iterator))
        for level in sorted(k for k in d.keys() if k > 0):
            d[level].append(d[level - 1][-1] - d[level - 1][-2])

        yield d[n - 1][-1]



if __name__ == '__main__':
    gen = delta(values=list(x ** 2 for x in range(30)), n=3)

    assert next(gen) == 2

    next(gen)

    # class Potion:
    #     def __init__(self, name):
    #         self.name = name
    #
    #     def __sub__(self, other):
    #         return Potion(other.name + self.name)
    #
    #
    # first_n = lambda g, n: [next(g) for _ in range(n)]
    #
    #
    # def ones():
    #     while True:
    #         yield 1
    #
    #
    # def up():
    #     a, b = 0, 1
    #     while True:
    #         yield a
    #         a, b = a + b, b + 3
    #
    #
    # assert delta([1, 2, 3, 4, 5, 6], 1) == [1, 1, 1, 1, 1]
    # assert delta([3, 3, -5, 77], 2) == [-8, 90]
    # assert delta([1.5] * 10, 9) == [0.0]
    # assert delta([1, -1, 1, -1], 3) == [-8]
    #
    # assert first_n(delta(up(), 1), 10) == [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]
    # assert first_n(delta(up(), 2), 10) == [3] * 10
    #
    # assert first_n(delta(ones(), 1), 1000) == [0] * 1000
    # assert first_n(delta(ones(), 100), 1000) == [0] * 1000
    #
    # input = [Potion("ko"), Potion("sham"), Potion("ro"), Potion("da")]
    #
    # assert [v.name for v in delta(input, 1)] == ["kosham", "shamro", "roda"]
    # assert [v.name for v in delta(input, 2)] == ["koshamshamro", "shamroroda"]
