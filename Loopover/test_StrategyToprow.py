import unittest
from Loopover.StrategyToprow import StrategyToprow
from Loopover.StrategyLiftshift import StrategyLiftshift
from Loopover.Cyclic_shift import Cyclic_shift_board

from Loopover.Row import Row, Node


def board(strboard):
    return [list(row) for row in strboard.split('\n')]


class TestStrategies(unittest.TestCase):

    def test_find_sort_graphs(self):
        target_row = ['A', 'B', 'C', 'D', 'E']
        row = Row([Node(i, v) for i, v in enumerate(['A', 'B', 'D', 'C', 'E'])], ind=0)

        # cyclic permutations of row for comparison in following solution
        # ['A', 'B', 'D', 'C', 'E']
        # ['B', 'D', 'C', 'E', 'A']
        # ['D', 'C', 'E', 'A', 'B']
        # ['C', 'E', 'A', 'B', 'D']
        # ['E', 'A', 'B', 'D', 'C']

        self.assertEqual(StrategyToprow.find_sort_graphs(row, target_row),
                         [{'C': 'D', 'D': 'C'},
                          {'A': 'B', 'B': 'D', 'D': 'E', 'E': 'A'},
                          {'A': 'D', 'B': 'C', 'C': 'E', 'D': 'A', 'E': 'B'},
                          {'A': 'C', 'B': 'E', 'C': 'A', 'D': 'B', 'E': 'D'},  # example 4
                          {'A': 'E', 'B': 'A', 'C': 'B', 'E': 'C'}])

    def test_split_subgraphs(self):
        # example 4 in test_find_sort_graphs
        self.assertEqual(StrategyToprow.split_subgraphs({'A': 'C', 'B': 'E', 'C': 'A', 'D': 'B', 'E': 'D'}),
                         [{'E': 'D', 'D': 'B', 'B': 'E'}, {'C': 'A', 'A': 'C'}])  # found two subgraphs

        # single graph
        self.assertEqual(StrategyToprow.split_subgraphs({'A': 'C', 'B': 'D', 'C': 'B', 'D': 'E', 'E': 'A'}),
                         [{'A': 'C', 'B': 'D', 'C': 'B', 'D': 'E', 'E': 'A'}])

        # two closed subgraphs
        self.assertTrue(StrategyToprow.split_subgraphs({'A': 'D', 'C': 'E', 'D': 'A', 'E': 'C'}) in \
                        ([{'A': 'D', 'D': 'A'}, {'C': 'E', 'E': 'C'}],
                         [{'C': 'E', 'E': 'C'}, {'A': 'D', 'D': 'A'}]))

    def test_choose_strategy_uneven(self):
        """even sized row can be used to adjust an uneven number of steps from subgraphs"""

        # only uneven number of steps across subgraphs
        uneven = [
            {'E': 'D', 'D': 'B', 'B': 'E', 'C': 'A', 'A': 'C'},  # 4 + 3 steps (two subg)
            {'F': 'B', 'B': 'F', 'E': 'A', 'A': 'D', 'D': 'E'},  # 3 + 4 steps (two subg)
            {'F': 'E', 'E': 'C', 'C': 'D', 'D': 'F'}  # 5 steps (single sub.)
        ]
        for strategy in uneven:
            c = Cyclic_shift_board(board('CEABDF\nGHIJKL\nMNOPQR'))
            c.solution = []  # reset previous solution
            c.solved_board = board('ABCDEF\nGHIJKL\nMNOPQR')
            Node.target = {val: (r, c) for r, row in enumerate(c.solved_board)
                           for c, val in enumerate(row)}

            # GET ALL STRATEGIES (this was used to generate uneven)
            # graphs = StrategyToprow.find_sort_graphs(
            #     row=c.rows[0],
            #     target_row=c.solved_board[0])
            #
            # # all subgraphs are found here:
            # subgraphs = [StrategyToprow.split_subgraphs(g) for g in graphs]
            #

            sortgraphs = StrategyToprow.choose_sort_strategy([strategy], target_row=c.solved_board[0])

            # TODO make test_choose_strategy independent from sort_by_subgraph!
            for g in sortgraphs:
                StrategyToprow.sort_by_subgraph(c, subgraph=g)

            # move A to the leftmost
            _, t = Node.current[c.solved_board[0][0]]
            c.rows[0].shift(c.rows[0].shortest_shiftLR(t, 0))

            self.assertEqual([row.toList() for row in c.rows], c.solved_board)

    def test_choose_strategy_uneven(self):
        """even number of total steps (even with multiple subgraphs present)
        pose viable solutions"""
        # even number of steps across subgraphs
        even = [{'F': 'D', 'D': 'A', 'A': 'F', 'E': 'B', 'B': 'C', 'C': 'E'},  # 4 + 4 steps (two subg)
                {'F': 'C', 'C': 'B', 'B': 'A', 'A': 'E', 'E': 'F'},  # 6 steps
                {'F': 'A', 'A': 'B', 'B': 'D', 'D': 'C', 'C': 'F'}]  # 6 steps

        for strategy in even:
            c = Cyclic_shift_board(board('CEABDF\nGHIJKL\nMNOPQR'))
            c.solution = []  # reset previous solution
            c.solved_board = board('ABCDEF\nGHIJKL\nMNOPQR')
            Node.target = {val: (r, c) for r, row in enumerate(c.solved_board)
                           for c, val in enumerate(row)}

            # GET ALL STRATEGIES (this was used to generate even)
            # graphs = StrategyToprow.find_sort_graphs(
            #     row=c.rows[0],
            #     target_row=c.solved_board[0])
            #
            # # all subgraphs are found here:
            # subgraphs = [StrategyToprow.split_subgraphs(g) for g in graphs]
            #

            sortgraphs = StrategyToprow.choose_sort_strategy([strategy], target_row=c.solved_board[0])
            # TODO make test_choose_strategy independent from sort_by_subgraph!
            for g in sortgraphs:
                StrategyToprow.sort_by_subgraph(c, subgraph=g)

            # move A to the leftmost
            _, t = Node.current[c.solved_board[0][0]]
            c.rows[0].shift(c.rows[0].shortest_shiftLR(t, 0))

            self.assertEqual([row.toList() for row in c.rows], c.solved_board)

    def test_toprow_example(self):
        # Test Case 0
        c = Cyclic_shift_board(board('ACDBE\nFGHIJ\nKLMNO\nPQRST'))
        c.solution = []  # reset previous solution
        c.solved_board = board('ABCDE\nFGHIJ\nKLMNO\nPQRST')
        Node.target = {val: (r, c) for r, row in enumerate(c.solved_board)
                       for c, val in enumerate(row)}

        StrategyToprow.executeStrategy(c)

        self.assertEqual([row.toList() for row in c.rows], c.solved_board)

        # Test Case 1
        c = Cyclic_shift_board(board('ACEBD\nFGHIJ\nKLMNO\nPQRST\nUVWXY'))

        c.solution = []  # reset previous solution
        c.solved_board = board('DBCAE\nFGHIJ\nKLMNO\nPQRST\nUVWXY')
        Node.target = {val: (r, c) for r, row in enumerate(c.solved_board)
                       for c, val in enumerate(row)}

        StrategyToprow.executeStrategy(c)

        self.assertEqual([row.toList() for row in c.rows], c.solved_board)

        if __name__ == '__main__':
            unittest.main(exit=False)
