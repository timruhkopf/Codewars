def memoize(func):
    def wrapper(n):
        if n in mem.keys():
            return mem[n]

        mem[n] = func(n)
        return mem[n]

    mem = {}
    return wrapper


@memoize
def fibonacci(n):
    if n in [0, 1]:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# (unittests) ------------------------------------------------------------------
import unittest


class MemFib(unittest.TestCase):
    def test_small_numbers(self):
        self.assertEqual(fibonacci(1), 1)

    def test_large_numbers(self):
        self.assertEqual(fibonacci(70), 190392490709135)
        self.assertEqual(fibonacci(60), 1548008755920)
        self.assertEqual(fibonacci(50), 12586269025)


if __name__ == '__main__':
    unittest.main(exit=False)
