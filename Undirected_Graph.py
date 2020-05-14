from collections import defaultdict


class Graph:
    """An undirected (acyclic) weighted graph
    https://www.codewars.com/kata/5aaea7a25084d71006000082"""

    def __init__(self, vertices_num):
        """
        :param vertices_num: number of nodes (an integer)
        """
        self.v = vertices_num
        self.nodes = ['A' + str(i) for i in range(vertices_num)]

    def adjmat_2_graph(self, adjm):
        """from adjacency matrix to dictionary"""
        return {self.nodes[r]: [(self.nodes[c], w) for c, w in enumerate(row) if w != 0]
                for r, row in enumerate(adjm)}

    def graph_2_mat(self, graph):
        """from dictionary to adjacency matrix"""
        g = defaultdict(int, {n: defaultdict(int, {k: w for k, w in vert}) for n, vert in graph.items()})
        return [[g[r][c] for c in self.nodes] for r in self.nodes]

    def graph_2_list(self, graph):
        """from dictionary to adjacency list"""
        return [[k, graph[k]] for k in sorted(graph.keys())]

    def list_2_graph(self, lst):
        """from adjacency list to dictionary"""
        return {k: v for k, v in lst}

    def mat_2_list(self, mat):
        """from adjacency matrix to adjacency list """
        return [[self.nodes[r], [(self.nodes[c], w) for c, w in enumerate(row) if w != 0]]
                for r, row in enumerate(mat)]

    def list_2_mat(self, lst):
        """from adjacency list to adjacency matrix"""
        return self.graph_2_mat(self.list_2_graph(lst))

    def find_all_paths(self, graph, start_vertex, end_vertex):
        """find all paths from node start_vertex to node end_vertex"""
        self.graph = graph
        self.paths = list()
        self.visited = [start_vertex]

        self._recursion_util(start_vertex, start_vertex, end_vertex)
        return sorted(sorted(self.paths, key=str), key=len)

    def _recursion_util(self, current_vertex, start_vertex, end_vertex):
        """helper method for self.find_all_paths"""
        if current_vertex == end_vertex:
            self.paths.append('-'.join(self.visited))
        elif len(self.visited) <= len(self.graph.keys()):
            for neighb, _ in self.graph[current_vertex]:
                if neighb not in self.visited:
                    self.visited.append(neighb)
                    self._recursion_util(neighb, start_vertex, end_vertex)
                    self.visited.remove(neighb)


if __name__ == '__main__':
    dct = {'A3': [('A0', 1), ('A2', 1)], 'A0': [('A3', 1), ('A2', 1)], 'A4': [('A2', 1)], 'A1': [('A2', 1)],
           'A2': [('A1', 1), ('A2', 1), ('A3', 1), ('A4', 1)]}
    g = Graph(5)
    assert g.find_all_paths(dct, "A0", "A4") == ['A0-A2-A4', 'A0-A3-A2-A4']

    # A dictionary is not ordered but the list of linked nodes is sorted
    graph = {'A0': [('A3', 1), ('A5', 4)],
             'A1': [('A2', 2)],
             'A2': [('A1', 1), ('A2', 2), ('A3', 1), ('A4', 1)],
             'A3': [('A0', 1), ('A2', 1)],
             'A4': [('A2', 1), ('A4', 1)],
             'A5': [('A3', 3)]}

    # adjacency matrix
    M = [[0, 0, 0, 1, 0, 4],
         [0, 0, 2, 0, 0, 0],
         [0, 1, 2, 1, 1, 0],
         [1, 0, 1, 0, 0, 0],
         [0, 0, 1, 0, 1, 0],
         [0, 0, 0, 3, 0, 0]]

    # adjacency list
    # L is sorted in order A0 to A5 and each sublist is sorted as in a graph dictionary
    L = [['A0', [('A3', 1), ('A5', 4)]],
         ['A1', [('A2', 2)]],
         ['A2', [('A1', 1), ('A2', 2), ('A3', 1), ('A4', 1)]],
         ['A3', [('A0', 1), ('A2', 1)]],
         ['A4', [('A2', 1), ('A4', 1)]],
         ['A5', [('A3', 3)]]]

    g = Graph(vertices_num=6)
    assert g.adjmat_2_graph(adjm=M) == graph
    assert g.graph_2_list(graph=graph) == L
    assert g.graph_2_mat(graph=graph) == M
    assert g.list_2_graph(lst=L) == graph
    assert g.mat_2_list(mat=M) == L
    assert g.list_2_mat(lst=L) == M
