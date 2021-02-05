import unittest
from Loopover.Row import Row, Column, Node


class TestRow(unittest.TestCase):

    def test_toList(self):

        row = Row([Node(position=(1, c), value=v) for c, v in enumerate('ABCDE')], ind=0, context=None)
        self.assertEqual(row.toList(), ['A', 'B', 'C', 'D', 'E'])

    def test_row_shift(self):
        class Context:
            solution = []

        context = Context() # to check the context awareness of Row

        row = Row([Node(position=(1, c), value=c) for c, node in enumerate(range(5))],
                  ind=0, context=context)
        row.shift(-1)
        self.assertEqual(context.solution, ['L0'])
        self.assertEqual(row.toList(), [1, 2, 3, 4, 0])

        col = Column([Node(position=(r, 1), value=r) for r, node in enumerate(range(5))],
                     ind=0, context=context)
        col.shift(-1)
        self.assertEqual(context.solution, ['L0', 'D0'])
        self.assertEqual(col.toList(), [1, 2, 3, 4, 0])

    def test_shortestLR(self):
        rowlen = 10
        row = Row([Node(position=(1, c), value=c) for c, node in enumerate(range(rowlen))], ind=0, context=None)
        self.assertEqual(row.shortest_shiftLR(0, 1), 1)  # L: -9, R:1
        self.assertEqual(row.shortest_shiftLR(1, 0), -1)  # L: -1, R: 9
        self.assertEqual(row.shortest_shiftLR(9, 0), 1)  # L: -9, R: 1
        self.assertEqual(row.shortest_shiftLR(0, 9), -1)  # L: -1, R: 9
        self.assertEqual(row.shortest_shiftLR(5, 3), -2)
        self.assertEqual(row.shortest_shiftLR(7, 2), -5)  # since left is first in min function


if __name__ == '__main__':
    unittest.main(exit=False)
