class Node:
    def __init__(self, position, symb):
        self.position = position
        self.symb = symb
        self.neighbours = []


class Graph:
    def __init__(self, map):
        # parsing
        m = map.split('\n')
        self.rdim = len(m[0])
        self.cdim = len(m)

        self.nodes = {(i, i // self.rdim): Node((i, i // self.rdim), symb)
                      for i, symb in enumerate(map.replace('\n', ''))}


    def connect_path(self, start=(0, 0), end=None):
        # Finding non cyclic paths: https://www.python.org/doc/essays/graphs/
        if end is None:
            pass
        pass

    def _find_neighbours(self, position):
        """returns the set of horizontal an vertical neighbours"""
        r, c = position
        cond = lambda r, c: 0 <= r < self.rdim and 0 <= c < self.cdim
        kernel = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        neighb = set((r + i, c + j) for i,j in kernel
                     if cond(r + i, c + j) and cond(r + i, c + j))
        return neighb

def path_finder(map):
    return Graph(map).connect_path(start=(0, 0))


if __name__ == '__main__':
    a = "\n".join([
        ".W.",
        ".W.",
        "..."
    ])

    b = "\n".join([
        ".W.",
        ".W.",
        "W.."
    ])

    c = "\n".join([
        "......",
        "......",
        "......",
        "......",
        "......",
        "......"
    ])

    d = "\n".join([
        "......",
        "......",
        "......",
        "......",
        ".....W",
        "....W."
    ])

    assert (path_finder(a) == True)
    assert (path_finder(b) == False)
    assert (path_finder(c) == True)
    assert (path_finder(d) == False)
