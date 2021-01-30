from Loopover.Row import Node

from itertools import cycle


class Algorithms:
    def liftshift(board, value):
        """first stage solving algorithm"""
        i, j = Node.current[value]
        r, c = Node.target[value]

        # (0) correct row & column
        if (i, j) == (r, c):
            return None

        # (1) correct row
        if i == r and j != c:
            board.cols[j].shift(1)
            board.cols[c].shift(1)
            board.rows[r - 1].shift(min([-(j + board.rdim - c), c - j], key=abs))  # FIXME: this one is faulty!!
            board.cols[j].shift(-1)
            board.cols[c].shift(-1)

        # (2) correct column
        elif j == c and i != r:
            board.rows[i].shift(-1)
            board.cols[c].shift(-(i - r))  # lift up
            board.rows[i].shift(1)
            board.cols[c].shift(i - r)  # lift down

        # (3) neither
        else:
            board.cols[c].shift(-(i - r))
            board.rows[i].shift(min([-(j + board.rdim + 1 - c), c - j], key=abs))
            board.cols[c].shift(i - r)

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

        graphs = list()
        for rot in rotations:
            # finding the misplaced leters and their target position's current occupant
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

        # corner case: sorted toprow
        _, t = Node.current[board.solved_board[0][0]]
        board.rows[0].shift(min(-t, board.rdim - t, key=abs))

        if [n.value for n in board.rows[0]] != board.solved_board[0]:

            # assuming there is a single, connected, odd numbered sorting graph:
            graph = Algorithms._find_misplaced(board.rows[0], board.solved_board[0])

            start, target = graph.popitem()
            r, c = Node.current[start]
            board.rows[0].shift(min(-c, board.rdim - c, key=abs))
            board.cols[0].shift(1)

            i = 0
            while start != target:
                if len(graph) >= 0:
                    _, t = Node.current[target]

                    board.rows[0].shift(min(-t, board.rdim - t, key=abs))
                    board.cols[0].shift([-1, 1][i % 2])

                    start = target
                    target = graph.pop(target)
                    i += 1







    # def _sort_toprow(board):  # , direct=-1):
    #     """second stage solving algorithm, a directed graph approach"""
    #     misplaced, ref = board._find_misplaced()
    #     if not bool(misplaced):
    #         return None  # _sort_toprow not needed
    #     start, target = misplaced.popitem()
    #
    #     # direct = -1
    #
    #     def initalisation(start):
    #         # align with reference - to find correct wild_occupies
    #         _, r = Node.current[ref]
    #         _, t = Node.target[ref]
    #         board.rows[0].shift(t - r)
    #
    #         _, s = Node.current[start]
    #         wild_occupies = board.solved_board[0][s]  # FIXME: must depend on the reference!
    #         board.rows[0].shift(min(-s, board.rdim - s, key=abs))
    #         board.cols[0].shift(-1)
    #         wildcard = board.rows[0][0].value
    #         misplaced[wild_occupies] = wildcard  # FIXME: can add a path if
    #         i = 0  # {-1: 0, 1: 1}[direct]
    #         return wildcard, i
    #
    #     wildcard, i = initalisation(start)
    #
    #     while start != target:
    #         print(board, '\n', start, '-->', target)
    #         _, t = Node.current[target]
    #         board.rows[0].shift(min(-t, board.rdim - t, key=abs))
    #         board.cols[0].shift([1, -1][i % 2])
    #
    #         start = target
    #         i += 1
    #
    #         if target == wildcard:
    #             if bool(misplaced):
    #                 start, target = misplaced.popitem()
    #                 # direct = -1
    #                 wildcard, i = initalisation(start)  # fixme: if twice in a row a wild card is hit, this fails
    #
    #         elif len(misplaced) > 0:
    #             target = misplaced.pop(start)
    #
    #     _, t = Node.current[board.solved_board[0][0]]
    #     board.rows[0].shift(-t)
    #     print(board, '\n')


if __name__ == '__main__':
    # check if the graphs are connected.
    assert Algorithms._is_connected_graph({'A': 'C', 'B': 'D', 'C': 'B', 'D': 'E', 'E': 'A'}) == True
    assert Algorithms._is_connected_graph({'A': 'D', 'C': 'E', 'D': 'A', 'E': 'C'}) == False
