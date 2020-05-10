from collections import deque
from itertools import chain


class Node:
    def __init__(self, position, value):
        self.position = position
        self.value = value


class Row(list):
    def __init__(self, *args):
        super(Row, self).__init__(*args)
        self.valqueue = deque(*args)  # TODO this argument allows shifting fairly easily
        # by popping the last argument and append from the other side

    def rowshift(self, direction):
        """:param direction: integer, either 0 (left) or 1 (right)"""

        if direction == 0:
            val = self.valqueue.popleft()
            self.valqueue.append(val)
        else:
            val = self.valqueue.pop()
            self.valqueue.appendleft(val)

        for node, v in zip(self, self.valqueue):
            node.value = v


class Cyclic_shift:
    direct = {'L': 0, 'R': 1, 'D': 0, 'U': 1}
    perspective = {'L': 'rows', 'R': 'rows', 'D': 'cols', 'U': 'cols'}

    def __init__(self, mixed_up_board, solved_board):
        """
        kata: https://www.codewars.com/kata/5c1d796370fee68b1e000611/train/python
        :param mixedUpBoard: two-dim arrays (or lists of lists) of symbols
        representing the initial (unsolved) grid
        :param solvedBoard:  same as mixedUpBoard but final (solved) grid.

        Different grid sizes are tested: from 2x2 to 9x9 grids
        (including rectangular grids like 4x5)
        """

        self.rows = [Row([Node((i, j), val) for i, row in enumerate(mixed_up_board) for j, val in enumerate(row)])]
        self.cols = [Row(col) for col in zip(*self.rows)]  # potentially reversed
        self.nodes = {node.position: node for node in chain(*self.rows)}

        self.board = {'rows': self.rows, 'cols': self.cols}
        self.solved_board = solved_board

    def __repr__(self):
        return ''.join([' '.join([str(self.nodes[(r, c)].value)
                                  for c in range(len(self.rows[0]))]) + '\n'
                        for r in range(len(self.rows))])

    def shift(self, direction):
        """:param direction: string such as L0, R1, D1, U2
        where L & R refer to rowshifts and D & U to column shifts"""
        direct, pos = tuple(direction)
        board = self.board[self.perspective[direct]]
        board[int(pos)].rowshift(direction=self.direct[direct])

    def solve(self):
        """Your task: return a List of moves that will transform the unsolved
        grid into the solved one. All values of the scrambled and unscrambled
        grids will be unique! Moves will be 2 character long Strings"""
        unsolvable = False
        if unsolvable:
            return None
        pass

    def check(self, moves):
        for move in moves:
            self.shift(move)

        board = [[self.nodes[(r, c)].value for c in range(len(self.rows[0]))]
                 for r in range(len(self.rows))]

        return board == self.solved_board


def loopover(mixed_up_board, solved_board):
    Cyclic_shift(mixed_up_board, solved_board)

    return None


if __name__ == '__main__':

    def run_test(start, end, unsolvable):
        def board(str):
            return [list(row) for row in str.split('\n')]

        # print_info(board(start), board(end))
        moves = loopover(board(start), board(end))
        if unsolvable:
            assert moves is None  # 'Unsolvable configuration

        else:
            assert Cyclic_shift(start, end).check(moves) == True
            # TODO write check function!


    # @test.it('Test 2x2 (1)')
    run_test('12\n34', '12\n34', False)

    # @test.it('Test 2x2 (2)')
    run_test('42\n31', '12\n34', False)

    # @test.it('Test 4x5')
    run_test('ACDBE\nFGHIJ\nKLMNO\nPQRST',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST', False)

    # @test.it('Test 5x5 (1)')
    run_test('ACDBE\nFGHIJ\nKLMNO\nPQRST\nUVWXY',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

    # @test.it('Test 5x5 (2)')

    run_test('ABCDE\nKGHIJ\nPLMNO\nFQRST\nUVWXY',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

    # @test.it('Test 5x5 (3)')
    run_test('CWMFJ\nORDBA\nNKGLY\nPHSVE\nXTQUI',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

    # @test.it('Test 5x5 (unsolvable)')
    run_test('WCMDJ\nORFBA\nKNGLY\nPHVSE\nTXQUI',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', True)

    # @test.it('Test 6x6')
    run_test('WCMDJ0\nORFBA1\nKNGLY2\nPHVSE3\nTXQUI4\nZ56789',
             'ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789', False)
