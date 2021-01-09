class Node:
    def __init__(self, position):
        self.position = position
        self.neighbours = []


class Graph:
    nodes = []
    def __init__(self, map):
        # parrsing

        # dim of map
        pass

    def connect_path(self, start=(0, 0), end=None):
        if end is None:
            pass
        pass

    def _find_neighbours(self, position):
        """returns the set of all neighbours (excluding self's position).
        all of them are bound checked"""
        r, c = position
        cond = lambda r, c: 0 <= r < self.rdim and 0 <= c < self.cdim
        kernel = (-1, 0, 1)
        neighb = set((r + i, c + j) for i in kernel for j in kernel
                     if cond(r + i, c + j) and cond(r + i, c + j) and i != j)
        return neighb

def path_finder(map):
    Graph(map).connect_path(start=(0,0))

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

    assert(path_finder(a) == True)
    assert(path_finder(b) == False)
    assert(path_finder(c) == True)
    assert(path_finder(d) == False)
