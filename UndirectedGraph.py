class Graph:
    """
    An undirected (acyclic) weighted graph
    https://www.codewars.com/kata/5aaea7a25084d71006000082"""

    def __init__(self, vertices_num):
        """
        breadth first & depth first algorithms can be found here:
        https://www.geeksforgeeks.org/find-if-there-is-a-path-between-two-vertices-in-a-given-graph/
        https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/
        :param vertices_num: number of nodes (an integer)
        """
        self.v = vertices_num

        # (maybe not useful here) : list of nodes from "A0", "A1" ... to "A index (vertices_num - 1)"
        self.nodes = None

    def adjmat_2_graph(self, adjm):
        """from adjacency matrix to dictionary"""
        pass

    def graph_2_mat(self, graph):
        """from dictionary to adjacency matrix"""
        pass

    def graph_2_list(self, graph):
        """from dictionary to adjacency list"""
        pass

    def list_2_graph(self, lst):
        """from adjacency list to dictionary"""
        pass

    def mat_2_list(self, mat):
        """from adjacency matrix to adjacency list """
        pass

    def list_2_mat(self, lst):
        """from adjacency list to adjacency matrix"""
        pass

    def find_all_paths(self, graph, start_vertex, end_vertex):
        """find all paths from node start_vertex to node end_vertex"""
        pass

if __name__ == '__main__':
    # check find all paths:
    dct = {'A3': [('A0', 1), ('A2', 1)], 'A0': [('A3', 1), ('A2', 1)], 'A4': [('A2', 1)], 'A1': [('A2', 1)],
           'A2': [('A1', 1), ('A2', 1), ('A3', 1), ('A4', 1)]}
    g = Graph(5)
    g.find_all_paths(dct, "A0", "A4")
    # returns l = ['A0-A2-A4', 'A0-A3-A2-A4']