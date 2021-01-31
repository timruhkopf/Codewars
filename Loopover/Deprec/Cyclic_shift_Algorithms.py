from Loopover.Row import Node
from itertools import cycle


class Algorithms:
    """THIS CLASS IS DEPREC, as it contains the less general (but original idea) of
    Loopover.StrategyToprow.py and is not split into the separate Strategies"""


    # (First Strategy) ---------------------------------------------------------
    def liftshift(board, value):
        """first stage solving algorithm, solves all but the first row, with three
        minor algorithms, depending on the respective position to the target
        :param value: str. letter, that is to be moved to its target position."""
        i, j = Node.current[value]
        r, c = Node.target[value]

        # (0) correct row & column
        if (i, j) == (r, c):
            return None

        # (1) correct row
        if i == r and j != c:
            board.cols[j].shift(1)
            board.cols[c].shift(1)
            board.rows[r - 1].shift(board.rows[r - 1].shortest_shiftLR(j, c))
            board.cols[j].shift(-1)
            board.cols[c].shift(-1)

        # (2) correct column
        elif j == c and i != r:
            board.rows[i].shift(-1)
            board.cols[c].shift(-(i - r))  # lift up # CONSIDER: Room for improvment: cols[c].shortest_shiftLR(i, r)
            board.rows[i].shift(1)
            board.cols[c].shift(i - r)  # lift down  # CONSIDER: Room for improvment: cols[c].shortest_shiftLR(r, i)

        # (3) neither
        else:
            board.cols[c].shift(-(i - r))
            board.rows[i].shift(board.rows[i].shortest_shiftLR(j, c))
            board.cols[c].shift(i - r)

    # (Second Strategy) --------------------------------------------------------
    @staticmethod
    def _is_connected_graph(graph):
        graph = graph.copy()
        start, target = graph.popitem()

        for i in range(len(graph)):
            if target in graph.keys():
                target = graph.pop(target)
            else:
                return False

        if start == target:
            return True

    @staticmethod
    def _find_misplaced(row, target_row):
        """check misalignement for each cyclic permutation and determine the
        (shortest single, connected & odd numbered) sorting graph
        :param row: the row to be sorted
        :param target_row: the
        :return dict: graph representation of the necessary operations to
        sort row to target_row"""

        # find the unique cyclic permutations
        cycs = cycle([n.value for n in row])
        rotations = list()
        for i in range(len(row)):
            rotations.append([next(cycs) for i in range(len(row))])
            next(cycs)

        # find the graph of sortings
        graphs = list()
        for rot in rotations:
            # finding the misplaced letters and their target position's current occupant
            graphs.append({x: y for x, y in zip(target_row, rot) if x != y})

        # check if there is any "single connected graph" with an odd number of steps.
        # this is the immediate solution.
        for g in (g for g in sorted(graphs, key=len) if len(g) % 2 != 0):
            if Algorithms._is_connected_graph(g):
                break
        else:
            print(graphs)
            raise ValueError('No single, odd numbered, connected graph was found')
        return g

        # original variant ------------------------------
        # _, current = Node.current[ref]
        # board.rows[0].shift(-current)
        # misplaced = {x: y for x, y in
        #              zip(board.solved_board[0], [v.value for v in board.rows[0]]) if x != y}

        # IDEA HERE: make the ref value match the position of the solved board -------------
        # THEN check which are not aligned. (the number of changes required likely changes, if any values are
        # consecutively soreted!)
        # for ref in board.solved_board[0]:
        #     _, c = Node.current[ref]
        #     _, t = Node.target[ref]
        #
        #     board.rows[0].shift(min(-(c - t), board.rdim - c + t))
        #
        #     print('\n', [n.value for n in board.rows[0]],
        #           '\n', board.solved_board[0])
        #     misplaced = {x: y for x, y in
        #                  zip(board.solved_board[0], [v.value for v in board.rows[0]]) if x != y}
        #
        #     print(ref, ':', len(misplaced), '\n\n')
        #
        #     if len(misplaced) % 2 != 0:
        #         return misplaced, ref
        #
        # # NO solution with uneven number of steps was found
        # return {}, board.solved_board[0][0]

    def sort_toprow(board):
        """
        A GRAPH APPROACH (EASY CASE)
        Given only the first row is not sorted, find a single conneced & odd numbered
        graph and shift according to that graph. Be careful with the wildcard
        ("card" that is not part of the toprow) introduced at the begining of this algo
        """
        if board.rows[0].toList() != board.solved_board[0]:
            # assuming there is a single, connected, odd numbered sorting graph:
            graph = Algorithms._find_misplaced(board.rows[0], board.solved_board[0])

            # initalisation step: first position in graph
            start, target = graph.popitem()
            _, s = Node.current[start]
            board.rows[0].shift(board.rows[0].shortest_shiftLR(s, 0))
            board.cols[0].shift(1)  # by convention

            # update graph: (with wildcard, it is no longer a circle)
            wild_occupies = start
            wildcard = board.rows[0][0].value
            for k, v in graph.items():
                if v == wild_occupies:
                    graph[k] = wildcard
                    break

            # walk down the graph and sort the row
            i = 0
            while start != target:
                _, t = Node.current[target]
                board.rows[0].shift(board.rows[0].shortest_shiftLR(t, 0))
                board.cols[0].shift([-1, 1][i % 2])

                start = target
                i += 1
                if len(graph) > 0:
                    target = graph.pop(target)

            # shift toprow such, that it is aligned with solution
            _, t = Node.current[board.solved_board[0][0]]
            board.rows[0].shift(board.rows[0].shortest_shiftLR(t, 0))


if __name__ == '__main__':
    # check if the graphs are connected.
    assert Algorithms._is_connected_graph({'A': 'C', 'B': 'D', 'C': 'B', 'D': 'E', 'E': 'A'}) == True
    assert Algorithms._is_connected_graph({'A': 'D', 'C': 'E', 'D': 'A', 'E': 'C'}) == False
