import inspect


class LazyInit(type):
    """
    A meta class to set all args and kwargs of init as instance.attributes
    https://www.codewars.com/kata/59b7b43b4f98a81b2d00000a
    """

    def __init__(cls, name, bases, dct):
        cls.__init__ = setkwargs(cls.__init__)


def setkwargs(method):
    """method decorator to attach the methods arguments to instance as attribute"""
    def wrapper(self, *args, **kwargs):

        # finding all arg names without self
        names = inspect.getfullargspec(method).args[1:]
        names = [n for n in names if n not in kwargs.keys()]

        self.__dict__.update(kwargs)
        self.__dict__.update({k: v for k, v in zip(names, args)})

        method(self, *args, **kwargs)

    return wrapper


if __name__ == '__main__':
    class Hello(metaclass=LazyInit):
        def __init__(self, a, b):
            self.c = 3  # check init of subclass is still executed

    c = Hello(a=1, b=2)
    d = Hello(3, b=4)  # case with args
    e = Hello(5,6)
    print(c.a, c.b)
    print(d.a, d.b)

    class Person(metaclass=LazyInit):
        def __init__(self, name, age): pass


    class Circle(metaclass=LazyInit):
        def __init__(self, x, ray): pass


    a_person = Person('Luke', 21)
    a_circle = Circle(1, 5)

    assert a_person.name == 'Luke'
    assert a_person.age == 21
    assert a_circle.x == 1
    assert a_circle.ray == 5
