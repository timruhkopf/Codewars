import unittest

from delta_generators import delta


class Test_delta(unittest.TestCase):

    def test_generator_1stdiff(self):
        # test for a generator
        gen = delta(values=(x ** 2 for x in range(30)), n=1)
        self.assertEqual([next(gen) for i in range(10)], [1, 3, 5, 7, 9, 11, 13, 15, 17, 19])

    def test_generator_2nddiff(self):
        gen = delta(values=(x ** 2 for x in range(30)), n=2)
        self.assertEqual([next(gen) for i in range(10)], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2])

    def test_list(self):
        gen = delta(values=list(x ** 2 for x in range(30)), n=3)
        self.assertEqual([next(gen) for i in range(10)], [0] * 10)

    def test_stopiteration(self):
        # notice, how higher differences must raise earlier (since there are fewer
        # elements at each subsequent level)
        gen = delta(values=(x ** 2 for x in range(10)), n=2)
        self.assertEqual(list(gen), [2] * 8)  # < -------

    # official tests -----------------------------------------------------------
    def test_simple_finite(self):
        self.assertEqual(list(delta([1, 2, 3, 4, 5, 6], 1)), [1, 1, 1, 1, 1])
        self.assertEqual(list(delta([3, 3, -5, 77], 2)), [-8, 90])
        self.assertEqual(list(delta([1.5] * 10, 9)), [0.0])
        self.assertEqual(list(delta([1, -1, 1, -1], 3)), [-8])

    def test_simple_infinite(self):
        first_n = lambda g, n: [next(g) for _ in range(n)]

        def ones():
            while True:
                yield 1

        self.assertEqual(first_n(delta(ones(), 1), 1000), [0] * 1000)
        self.assertEqual(first_n(delta(ones(), 100), 1000), [0] * 1000)

        def up():
            a, b = 0, 1
            while True:
                yield a
                a, b = a + b, b + 3

        self.assertEqual(first_n(delta(up(), 1), 10), [1, 4, 7, 10, 13, 16, 19, 22, 25, 28])
        self.assertEqual(first_n(delta(up(), 2), 10), [3] * 10)

    def test_other_types(self):
        class Potion:
            def __init__(self, name):
                self.name = name

            def __sub__(self, other):
                return Potion(other.name + self.name)

        input = [set([6, 2, 'A']), set([2, 'B', 8]), set(['A', 'B'])]
        self.assertEqual(list(delta(input, 1)), [{8, 'B'}, {'A'}])
        self.assertEqual(list(delta(input, 2)), [{'A'}])

        input = [Potion("ko"), Potion("sham"), Potion("ro"), Potion("da")]
        self.assertEqual([v.name for v in delta(input, 1)], ["kosham", "shamro", "roda"])
        self.assertEqual([v.name for v in delta(input, 2)], ["koshamshamro", "shamroroda"])


if __name__ == '__main__':
    unittest.main(exit=False)
