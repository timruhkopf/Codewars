from collections import defaultdict


class Graph:
    """An undirected (acyclic) weighted graph
    https://www.codewars.com/kata/5aaea7a25084d71006000082"""

    def __init__(self, vertices_num):
        """
        breadth first & depth first algorithms can be found here:
        https://www.geeksforgeeks.org/find-if-there-is-a-path-between-two-vertices-in-a-given-graph/
        https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
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
        pass

if __name__ == '__main__':
    # dictionary
    # A dictionary is not ordered but the list of linked nodes is sorted
    graph = {'A0': [('A3', 1), ('A5', 4)], 'A1': [('A2', 2)], 'A2': [('A1', 1), ('A2', 2), ('A3', 1), ('A4', 1)],
             'A3': [('A0', 1), ('A2', 1)], 'A4': [('A2', 1), ('A4', 1)], 'A5': [('A3', 3)]}

    # adjacency matrix
    M = [[0, 0, 0, 1, 0, 4], [0, 0, 2, 0, 0, 0], [0, 1, 2, 1, 1, 0], [1, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0],
         [0, 0, 0, 3, 0, 0]]

    # adjacency list
    # L is sorted in order A0 to A5 and each sublist is sorted as in a graph dictionary
    L = [['A0', [('A3', 1), ('A5', 4)]], ['A1', [('A2', 2)]], ['A2', [('A1', 1), ('A2', 2), ('A3', 1), ('A4', 1)]],
         ['A3', [('A0', 1), ('A2', 1)]], ['A4', [('A2', 1), ('A4', 1)]], ['A5', [('A3', 3)]]]

    g = Graph(vertices_num=6)
    assert g.adjmat_2_graph(adjm=M) == graph
    assert g.graph_2_list(graph=graph) == L
    assert g.graph_2_mat(graph=graph) == M
    assert g.list_2_graph(lst=L) == graph
    assert g.mat_2_list(mat=M) == L
    assert g.list_2_mat(lst=L) == M

    dct = {'A3': [('A0', 1), ('A2', 1)], 'A0': [('A3', 1), ('A2', 1)], 'A4': [('A2', 1)], 'A1': [('A2', 1)],
           'A2': [('A1', 1), ('A2', 1), ('A3', 1), ('A4', 1)]}
    g = Graph(5)
    g.find_all_paths(dct, "A0", "A4")
    # returns l = ['A0-A2-A4', 'A0-A3-A2-A4']
