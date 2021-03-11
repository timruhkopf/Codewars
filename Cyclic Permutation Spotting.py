from typing import Tuple


def is_cyclic(p: Tuple[Tuple[int]]) -> bool:
    l = [p[0][0], p[1][0]]
    ind = p[0].index(l[-1])

    while l[-1] != p[0][0]:
        l.extend([p[0][ind], p[1][ind]])
        ind = p[0].index(l[-1])

    check = [i in l for i in p[0]]
    return all(check)


if __name__ == '__main__':
    p = (
        (1, 2, 3, 4, 5, 6),
        (4, 3, 6, 2, 1, 5)
    )
    assert is_cyclic(p) == True
