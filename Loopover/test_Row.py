import unittest
from Loopover.Row import Row, Node


class TestRow(unittest.TestCase):

    def test_row_shift(self):
        # row = Row([Node(position=(1, c), value=c) for c, node in enumerate(range(5))], ind=0, row=True)
        # print(row)
        # row.shift(-1)
        # print(row)
        # Row.Solution

        # len(row)
        #
        # col = Row([Node(position=(r, 1), value=r) for r, node in enumerate(range(5))], ind=0, row=False)
        # print(col)
        # col.shift(-1)
        # print(col)
        #
        # len(col)
        pass

    def test_shortestLR(self):
        # rowlen = 10
        # row = Row([Node(position=(1, c), value=c) for c, node in enumerate(range(rowlen))], ind=0, row=True)
        # assert row.shortest_shiftLR(0, 1) == 1  # L: -9, R:1
        # assert row.shortest_shiftLR(1, 0) == -1  # L: -1, R: 9
        # assert row.shortest_shiftLR(9, 0) == 1  # L: -9, R: 1
        # assert row.shortest_shiftLR(0, 9) == -1  # L: -1, R: 9
        # assert row.shortest_shiftLR(5, 3) == -2
        # assert row.shortest_shiftLR(7, 2) == -5  # since left is first in min function
        pass

    def test_toList(self):
        # check toList
        # row = Row([Node(position=(1, c), value=v) for c, v in enumerate('ABCDE')], ind=0, row=True)
        # assert row.toList() == ['A', 'B', 'C', 'D', 'E']
        pass


if __name__ == '__main__':
    unittest.main()
