from itertools import cycle
from Loopover.Row import Node


class StrategyToprow:
    def executeStrategy(board):
        """This strategy solves the toprow of the board, by analysing the
        possible sortings (sorting graphs) and choosing a short """
        # Consider yield strategies rather than precomputing all strategies.
        #  this is slightly more computiational efficient, but the solution added
        #  by StrategyToprow is not necessarily the shortest.


        graphs = StrategyToprow.find_sort_graphs(
            row=board.rows[0],
            target_row=board.solved_board[0])
        sortgraphs = StrategyToprow.choose_sort_strategy(graphs, target_row=board.solved_board[0])

        # if sortgraphs is None:
        #     # No strategy can be successful, this board is unsolvable
        #     return None

        # Consider: shortest available addition to solution:
        # if StrategyToprow.choose_sort_strategy returned the list of valid
        # strategies (remove invalid & add turnovers where necessary)
        # min(sortgraphs, key=lambda g: sum(sum([len(subgraph) + 1 for subgraph in g])
        for g in sortgraphs:
            StrategyToprow.sort_by_subgraph(board, subgraph=g)

        _, t = Node.current[board.solved_board[0][0]]
        board.rows[0].shift(board.rows[0].shortest_shiftLR(t, 0))

    # (Preprocessing of available strategies) ----------------------------------
    @staticmethod
    def find_sort_graphs(row, target_row):
        # find the unique cyclic permutations of row
        cycs = cycle(row.toList())
        rotations = list()
        for i in range(len(row)):
            rotations.append([next(cycs) for i in range(len(row))])
            next(cycs)

        # find the graph of sortings (e.g. A --> C, C --> B, B --> A)
        graphs = list()
        for rot in rotations:
            # finding the misplaced letters and their target position's current occupant
            graphs.append({x: y for x, y in zip(target_row, rot) if x != y})

        return graphs

    @staticmethod
    def split_subgraphs(graph):
        """
        :param graph: dict, directed and linear (cyclic) graph(s); a graph
        may contain multiple closed subgraphs: {'A': 'D', 'C': 'E', 'D': 'A', 'E': 'C'}
        :return: list of dict, which is a list of the closed subgraphs.
        """
        graph = graph.copy()
        start, target = graph.popitem()

        subgraphs = list()
        subg = {start: target}

        while len(graph) > 0:  # for i in range(len(graph)):
            if target in graph.keys():
                start = target
                target = graph.pop(start)

                subg.update({start: target})

            if target in subg.keys():  # closed the circle (subgraph)
                subgraphs.append(subg)

                if len(graph) > 0:
                    start, target = graph.popitem()
                    subg = {start: target}

        return subgraphs

    @staticmethod
    def choose_sort_strategy(graphs, target_row):
        """we search for a short graph """
        for g in sorted(graphs, key=len):
            subgraphs = StrategyToprow.split_subgraphs(g)

            if sum([len(s) + 1 for s in subgraphs]) % 2 == 0:
                # (+1: since the initalisation step requires an additional turn)
                return subgraphs
            elif len(g) % 2 != 0 and (sum([len(s) + 1 for s in subgraphs]) + len(g)) % 2 == 0:
                # do a total turnover afterwards (A->B B->C C->A), to even the total number of
                # turns. this is only possible for uneven length rows (g)
                turnover = {s: t for s, t in zip(target_row, target_row[1:])}
                turnover.update({target_row[-1]: target_row[0]})
                subgraphs.append(turnover)
                return subgraphs

    # (execute a subgraph) -----------------------------------------------------
    def sort_by_subgraph(board, subgraph):
        # FIXME: need to access the Node.target via board not via import of Node
        if len(board.solution) > 1 and 'U0' == board.solution[-1]:  # check if last switch of first column was up
            i, first_move = 1, -1
        else:
            i, first_move = 0, 1

        # initalisation step: first position in graph
        start, target = subgraph.popitem()
        _, s = Node.current[start]
        board.rows[0].shift(board.rows[0].shortest_shiftLR(s, 0))
        board.cols[0].shift(first_move)  # by convention

        # update graph: (with wildcard, it is no longer a circle)
        wild_occupies = start
        wildcard = board.rows[0][0].value
        for k, v in subgraph.items():
            if v == wild_occupies:
                subgraph[k] = wildcard
                break

        while start != target:
            _, t = Node.current[target]
            board.rows[0].shift(board.rows[0].shortest_shiftLR(t, 0))
            board.cols[0].shift([-1, 1][i % 2])

            start = target
            i += 1
            if len(subgraph) > 0:
                target = subgraph.pop(target)


if __name__ == '__main__':
    # (find_sort_graphs) -------------------------------------------------------
    target_row = ['A', 'B', 'C', 'D', 'E']
    row = ['B', 'C', 'D', 'E', 'A']  # single shift right suffices

    row = ['B', 'E', 'A', 'C', 'D']

    # (split_subgraphs) ------------------------------------------------
    # single graph
    assert StrategyToprow.split_subgraphs({'A': 'C', 'B': 'D', 'C': 'B', 'D': 'E', 'E': 'A'}) == \
           [{'A': 'C', 'B': 'D', 'C': 'B', 'D': 'E', 'E': 'A'}]

    # two closed subgraphs
    assert StrategyToprow.split_subgraphs({'A': 'D', 'C': 'E', 'D': 'A', 'E': 'C'}) in \
           ([{'A': 'D', 'D': 'A', }, {'C': 'E', 'E': 'C'}],
            [{'C': 'E', 'E': 'C'}, {'A': 'D', 'D': 'A', }])
