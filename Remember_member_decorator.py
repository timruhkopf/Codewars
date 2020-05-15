class Meta(type):

    def __new__(cls, name, bases, dct):
        newcls = super().__new__(cls, name, bases, dct)
        newcls.instances = dict()
        return newcls

    def __getitem__(cls, item):
        if isinstance(item, int):
            item = (item,)
        return cls.instances[item]

    def __iter__(cls):
        return cls

    def __next__(cls):
        if not hasattr(cls, '_iter'):
            cls._iter = iter([k if len(k) != 1 else k[0] for k in sorted(cls.instances.keys(), key=len)])
        return next(cls._iter)


def remember(cls):
    cls = Meta(cls.__name__, cls.__bases__, {k: v for k, v in cls.__dict__.items()})

    def __new__(cls, *args):
        # to ensure same init referes to the same object
        if args not in cls.instances.keys():
            instance = super(cls, cls).__new__(cls)
            cls.instances[args] = instance
            return instance
        else:
            return cls.instances[args]

    cls.__new__ = __new__
    return cls


if __name__ == '__main__':
    @remember
    class A(object):
        def __init__(self, x, y=0, z=0):
            pass


    a = A(1)
    b = A(2, 3)
    b2 = A(2, 3)
    c = A(4, 5, 6)
    d = A(1)

    # subscripting works
    assert A[2, 3] is b
    assert A[4, 5, 6] is c

    # objects with same initialization are same
    assert A[2, 3] is b is b2
    assert A[1] is a is d

    # object is iterable
    assert {x for x in A}, {1, (2, 3), (4, 5, 6)}


    @remember
    class B(object):
        def __init__(self, *args):
            pass

    B()
    B(1, 2)
    B(7)

    assert {x for x in B}, {(), (1,2), 7}
