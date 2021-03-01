from itertools import cycle

from ..Board.Row import Node


class StrategyToprow_short:
    def execute_strategy(board):
        graph = StrategyToprow_short.find_sort_graphs(board)
        StrategyToprow_short.sort_toprow(board, graph)

    def find_sort_graphs(board):
        row = board.rows[0]
        cycs = cycle(row.toList())
        rotations = list()
        for i in range(len(row)):
            rotations.append([next(cycs) for i in range(len(row))])
            next(cycs)

        # find the graph of sortings (e.g. A --> C, C --> B, B --> A)
        for rot in rotations:
            # finding the misplaced letters and their target position's current occupant
            yield {x: y for x, y in zip(row, rot) if x != y}

    def sort_toprow(board, graph):
        """
        TODO : this 'ignorant' approach can only work if transpose is available & the
         all sorting graphs (even consisting of multiple subgraphs) pose valid solutions
         (added a full turnover where necessary)
        Given only the first row is not sorted, find a single conneced & odd numbered
        graph and shift according to that graph. Be careful with the wildcard
        ("card" that is not part of the toprow) introduced at the begining of this algo
        """
        if board.rows[0].toList() != board.solved_board[0]:
            # assuming there is a single, connected, odd numbered sorting graph:

            # initalisation step: first position in graph
            start, target = graph.popitem()
            _, s = Node.current[start]
            board.rows[0].shift(board.rows[0].shortest_shiftLR(s, 0))
            board.cols[0].shift(1)  # by convention
            # TODO look at solution[-1] if it is up, start here with down (
            #  -1). in that case also change i to 1 in while init.

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

            else:
                # todo when the only a subgraph is executed (len(graph) >0 here!
                #  execute sort_toprow on the remaining subgraph!
                #  if that does not suffice (uneven number of total steps)
                #  make a full turnover . Now check if solution is valid -
                #  if not, it is unsolvable
                pass

            # shift toprow such, that it is aligned with solution
            _, t = Node.current[board.solved_board[0][0]]
            board.rows[0].shift(board.rows[0].shortest_shiftLR(t, 0))
