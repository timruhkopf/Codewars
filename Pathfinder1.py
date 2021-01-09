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
