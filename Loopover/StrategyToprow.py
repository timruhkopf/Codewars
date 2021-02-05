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

        if sortgraphs is not None:
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
        """
        This function looks at the unique cyclic permutations of row
        and compares each of them against the target row. Given the current
        permutation it determines where each of the Letters in row need to move
        (the position of row's permutation occupant)

        e.g. permutation of row = ['C', 'A', 'B'], target_row = ['A', 'B', 'C']
        C --> B, B --> A,  A --> C (letter C needs to move to B's current position, ...)
        so this permutation has the sort graph {C: B, B: A, A: C}

        :param row: Row object.
        :param target_row: List.
        :return: list of dicts.
        """
        # find the unique cyclic permutations of row. using cycle avoids unnecessary
        # appends to the solution + no dependency to Cyclic_shift_board
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
        """
        Viable solutions are those that produce an even number of steps in total.
        Since sort_by_subgraph algorithm uses len(subgraph) + 1 steps, the following solutions
        work:

            1) a single closed graphs of uneven length: e.g. {'B': 'C', 'C': 'D', 'D': 'B'}.
               The total number of steps is 4 and even, which puts the wildcard
               (see sort_by_subgraph doc for details) in its correct place after
               the execution of the graph.

            2) multiple closed subgraphs, if
                a) they produce an even number of steps in total and the first
                    overall move and the last overall move cancel.
                b) the total number of steps is uneven and the length of the row
                    is even. e.g.: [{'E': 'D', 'D': 'B', 'B': 'E'}, {'C': 'A', 'A': 'C'}]
                    with row = [C, E, A, B, D, F]
                    (remember: each subgraph requires len(subgraph)+1 steps)
                    In this case, the entire row can be rearanged
                    {A:B, B:C, C:D, D:A}, adding an uneven number of steps
                    --> returns to case 2a)

        if there is no graph (or collection of subgraphs), that can create
        an even number of steps (e.g. 2b) but with no

        :param graphs: list of dicts. [{A:B B:A}, {A:C, C:B: B:A}]
        :param target_row: list. target format
        :return:
            list of dict(s). describes an entire graph (can be composed of
            closed subgraphs), which is a valid strategy.
            None. if there is no valid strategy

        """
        # prefers strategies, whose total number of steps is even and prefers overall shorter strategies.
        # sorted(graphs, key=lambda x: (len(x) % 2 == 0, len(x))) # not applicable
        for g in sorted(graphs, key=len):
            subgraphs = StrategyToprow.split_subgraphs(g)
            print(subgraphs, sum([len(s) + 1 for s in subgraphs]))
            # simple solution even number of steps across subgraph(s)
            if sum([len(s) + 1 for s in subgraphs]) % 2 == 0:
                # even number of total steps, immediate solution; execute all subgraphs
                # (len(s) +1: since the initialisation step requires an additional turn)
                return subgraphs

            # uneven number of total steps across multiple subgraphs, but! rowlen is even
            # - adds uneven no of steps
            elif len(target_row) % 2 == 0:
                # do a total turnover afterwards (A->B B->C C->D D->A),
                # to even the total number of steps.
                turnover = {s: t for s, t in zip(target_row, target_row[1:])}
                turnover.update({target_row[-1]: target_row[0]})
                subgraphs.append(turnover)
                return subgraphs

        else:
            return None

    # (execute a subgraph) -----------------------------------------------------
    def sort_by_subgraph(board, subgraph):
        """
        Execute the subgraph strategy:
        e.g. subgraph {'A': 'B', 'B': 'D', 'D': 'E', 'E': 'A'}
        1) initialise the algorithm (two column moves):
            shift A to the leftmost position (0,0) and push it up -
            so a wildcard lies on A's old position now. shift B (A's target)
            to 0,0. push A down on B's position. B is the new start

        2) shift D to the leftmost and push B up on D's position.
        shift E (D's Target) to the leftmost and push D down on E's position
        shift the Wildcard (occupies A's space and is E's target) to the leftmost.
        push E up on the wildcard's position.

        Notice how the order of up and down is interchangeable! (we could start
        the algorithm with down.

        The total number of steps is 5 (uneven), Because the initialisation took
        two steps and each following sorting a single step. The subgraph is
        length 4 (even), so the no. of steps is, uneven. As consequence, the
        wildcard in this example is misplaced after execution.
        StrategyToprow.choose_sort_strategy wisely! ;)

        # Consecutive calls to sort_subgraph:
        e.g. the two subgraphs [{'A': 'D', 'D': 'A'}, {'C': 'E', 'E': 'C'}]
        are executed. {'A': 'D', 'D': 'A'} causes u, d, u. To ensure, that the
        wildcard is pushed down (if it was pushed up in the first subgraph's first move)
        in the last subgraph's last step (and thereby placed correctly!),
        the second subgraph must start with d (second subgraph executes d, u, d).
        This is accounted for by looking at the board.solution's last execution.

        :param subgraph: dict. a closed subgraph e.g. {A: B, B: A}
        :return: None: changes the state of board
        """
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
