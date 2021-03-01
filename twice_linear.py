import time
from collections import deque

def timing_val(func):
    def wrapper(*arg, **kw):
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        print((t2 - t1))
        return res
    return wrapper

class Twice_linear:
    """https://www.codewars.com/kata/5672682212c8ecf83e000050/"""
    u = deque([1])
    dq = {'ys': deque([3]), 'zs': deque([4])}
    y= lambda self, x: 2 * x + 1
    z= lambda self, x: 3 * x + 1
    selector = ['ys', 'zs']

    def _continue(self, n):
        while len(self.u) < n+1:
            x = self.dq[self.selector[self.dq['zs'][0] < self.dq['ys'][0]]].popleft()
            self.dq['ys'].append(self.y(x))
            self.dq['zs'].append(self.z(x))

            # prevent doubles
            if self.u[-1] != x:
                self.u.append(x)

            continue

        return self.u[n]


T = Twice_linear()

@timing_val
def dbl_linear(n):
    return T._continue(n)


if __name__ == '__main__':
    us = [1, 3, 4, 7, 9, 10, 13, 15, 19, 21, 22, 27]

    assert dbl_linear(n=12) == 27
