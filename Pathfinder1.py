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

        tupler = lambda i: (i // self.rdim, i % self.rdim)
        self.nodes = {tupler(i): Node(tupler(i), symb)
                      for i, symb in enumerate(map.replace('\n', ''))}

        for node in [node for node in self.nodes.values() if node.symb != 'W']:
            node.neighbours = [pos for pos in self._find_neighbours(node.position)
                               if self.nodes[pos].symb != 'W']

        # [(node.position, node.neighbours) for node in self.nodes.values()]

        self.end = (self.rdim - 1, self.cdim - 1)
        self.start = (0, 0)

    def connect_path(self, start=(0, 0), path=[], end=None):
        """In a backtracking manner find weather or not their is a path beween start and end"""
        path = path + [start]
        if start == end:
            return path
        for neighb in sorted(self.nodes[start].neighbours, key= lambda x: x[0], reverse=True):
            if neighb not in path:
                newpath = self.connect_path(start=neighb, path=path, end=end)
                if newpath:
                    return newpath
        return None

    def find_path(self):
        return self.connect_path(start=self.end, end=self.start)


    def _find_neighbours(self, position):
        """returns the set of horizontal an vertical neighbours"""
        r, c = position
        cond = lambda r, c: 0 <= r < self.rdim and 0 <= c < self.cdim
        kernel = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        neighb = set((r + i, c + j) for i, j in kernel
                     if cond(r + i, c + j) and cond(r + i, c + j))
        return neighb


def path_finder(map):
    return bool(Graph(map).find_path())


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
