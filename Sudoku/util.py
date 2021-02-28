import time


def timeit(method):
    def wrapper(ref, *args, **kwargs):  # method can have arguments. ref is B's self!
        start = time.time()
        result = method(ref, *args, **kwargs)
        end = time.time()
        print(end - start)
        return result

    return wrapper


def count_calls(method):
    def wrapper(ref, *args, **kwargs):  # method can have arguments. ref is B's self!
        wrapper.calls += 1
        return method(ref, *args, **kwargs)

    wrapper.calls = 0
    return wrapper
