class Vector(object):

    def __init__(self, iterable):
        self._vec = tuple(x for x in iterable)
        self.len = self._vec.__len__()

    def __str__(self):
        return str(tuple(self._vec)).replace(' ', '')

    def __repr__(self):
        return self._vec.__repr__()

    def __iter__(self):
        return iter(self._vec)

    def check_compatible(func):
        def wrapper(self, other):
            assert (isinstance(other, Vector))
            assert (other.len == other.len)
            return func(self, other)

        return wrapper

    def norm(self):
        return sum(a ** 2 for a in self._vec) ** 0.5

    @check_compatible
    def add(self, b):
        return Vector(a + b for a, b in zip(self._vec, b._vec))

    @check_compatible
    def subtract(self, b):
        return Vector(a - b for a, b in zip(self._vec, b._vec))

    @check_compatible
    def dot(self, b):
        return sum(a * b for a, b in zip(self._vec, b._vec))

    @check_compatible
    def equals(self, b):
        return self._vec == b._vec


if __name__ == '__main__':
    """
    If you try to add, subtract, or dot two vectors with different lengths, you must throw an error
    Also provide:
    a toString method, so that using the vectors from above, a.toString() === '(1,2,3)' (in Python, this is a __str__ method, so that str(a) == '(1,2,3)')
    an equals method, to check that two vectors that have the same components are equal
    Note: the test cases will utilize the user-provided equals method.
    """
    a = Vector([1, 2, 3])
    b = Vector([3, 4, 5])
    c = Vector([5, 6, 7, 8])

    a.add(b)  # should return a new Vector([4, 6, 8])
    a.subtract(b)  # should return a new Vector([-2, -2, -2])
    a.dot(b)  # should return 1*3 + 2*4 + 3*5 = 26
    a.norm()  # should return sqrt(1^2 + 2^2 + 3^2) = sqrt(14)
    # a.add(c)  # raises an exception

    a = Vector([1, 2])
    b = Vector([3, 4])
    print(str(a))
    a.add(b).equals(Vector([4, 6]))

    a = Vector([1, 2, 3])
    b = Vector([3, 4, 5])

    a.add(b).equals(Vector([4, 6, 8]))
    a.subtract(b).equals(Vector([-2, -2, -2]))
    a.dot(b), 26
    a.norm(), 14 ** 0.5

    # check iter method works as expected
    list(a + b for a, b in zip(a, b))
