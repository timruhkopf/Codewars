class Graph:
    def __init__(self, V):
        """
        https://www.codewars.com/kata/58867e2e2d2177547500007f
        Initialize an empty graph with v vertices(V) and 0 edges(E).
        :raises IllegalArgumentError unless 0 <= V"""
        if V < 0:
            raise IllegalArgumentError()

        self.V = V
        self.E = 0
        self.adj = [[] for v in range(V)]

    def add_edge(self, V, W):
        """
        Add the undirected edge v-w to this graph.
        :raise IllegalArgumentError unless both 0 <= v < V and 0 <= w < V
        """
        if not 0 <= V < self.V or not 0 <= W < self.V:
            raise IllegalArgumentError()

        self.E += 1

        self.adj[V].append(W)
        self.adj[W].append(V)


class IllegalArgumentError(Exception):
    def __init__(self):
        pass
        # self.str = "Value of {variable} out of bounds, " \
        #            "should be: {lower} <= {variable}".format(
        #     variable=variable, lower=lower)
        #
        # if upper is not None:
        #     ''.joint((self.str, ' < {upper}'.format(upper=upper)))

    def __str__(self):
        return self.str


if __name__ == '__main__':
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(2, 2)

    assert g.V == 3
    assert g.E == 2
    assert g.adj == [[1], [0], [2, 2]]

    g = Graph(4)
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(0, 2)

    assert g.adj == [[1, 3, 2], [0], [0], [0]]
