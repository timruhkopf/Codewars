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


def path_finder(map):
    Graph(map).connect_path(start=(0, 0))


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
