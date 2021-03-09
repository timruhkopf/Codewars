import types


def delta(values, n):
    if isinstance(values, types.GeneratorType):
        a = next(values)
        while True:
            b = next(values)
            yield b - a
            a = b
    else:
        ret = values.copy()
        for i in range(n):
            ret = [i[1] - i[0] for i in zip(ret, ret[1::])]
        return ret


if __name__ == '__main__':
    class Potion:
        def __init__(self, name):
            self.name = name

        def __sub__(self, other):
            return Potion(other.name + self.name)


    first_n = lambda g, n: [next(g) for _ in range(n)]


    def ones():
        while True:
            yield 1


    def up():
        a, b = 0, 1
        while True:
            yield a
            a, b = a + b, b + 3


    assert delta([1, 2, 3, 4, 5, 6], 1) == [1, 1, 1, 1, 1]
    assert delta([3, 3, -5, 77], 2) == [-8, 90]
    assert delta([1.5] * 10, 9) == [0.0]
    assert delta([1, -1, 1, -1], 3) == [-8]

    assert first_n(delta(up(), 1), 10) == [1, 4, 7, 10, 13, 16, 19, 22, 25, 28]
    assert first_n(delta(up(), 2), 10) == [3] * 10

    assert first_n(delta(ones(), 1), 1000) == [0] * 1000
    assert first_n(delta(ones(), 100), 1000) == [0] * 1000

    input = [Potion("ko"), Potion("sham"), Potion("ro"), Potion("da")]

    assert [v.name for v in delta(input, 1)] == ["kosham", "shamro", "roda"]
    assert [v.name for v in delta(input, 2)] == ["koshamshamro", "shamroroda"]
