from collections import deque
from itertools import chain


def loopover(mixed_up_board, solved_board):
    return Cyclic_shift(mixed_up_board, solved_board).solve()


class Node:
    current = dict()
    target = dict()  # target coordinates value: (row, col)

    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __repr__(self):
        return str(self.value)


class Row(list):
    Solution = list()
    direct = {True: ('L', 'R'), False: ('D', 'U')}

    def __init__(self, iterable, ind, row=True):
        """:param iterable: an ordered collection of Node instances
        :param ind: row index of this row
        :param row: boolean: if i am row or column"""
        super(Row, self).__init__(iterable)
        self.queue = deque(maxlen=len(iterable))

        # Identifyer of row object!
        self.row = row  # am i a row?
        self.ind = str(ind)  # row / column index

    def rowshift(self, direction):
        """:param direction: integer. value of integer indicates the number of
        repeated shifts. the sign indicates a left(-) or right(+) shift"""
        self.queue.extend([node.value for node in self])  # overwrites at each step the queue
        self.queue.rotate(direction)

        self.Solution.extend(self.direction_parser(direction))

        for node, v in zip(self, self.queue):
            node.value = v
            Node.current[v] = node.position  # still efficient as merely pointer
            # to immutable tuple is shared (no new tuple is created)

    def direction_parser(self, direction):
        """:param direction: integer: number of shifts, left shift is negative, right positive"""
        return [self.direct[self.row][direction < 0] + self.ind] * abs(direction)


class Cyclic_shift:
    direct = {'L': -1, 'R': 1, 'D': 1, 'U': -1}
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

        # Consider: translating latters to numbers (as modulo devision allows immediate
        # calculation of the target position. also this allows to ).
        # Make the Node aware of (/allow to inquire) where the target of the currently occupying value is.
        Node.current = {val: (r, c) for r, row in enumerate(mixed_up_board) for c, val in enumerate(row)}
        Node.target = {val: (r, c) for r, row in enumerate(solved_board) for c, val in enumerate(row)}

        # Create a playable board
        self.rows = [Row([Node((r, c), val) for c, val in enumerate(row)], r, True) for r, row in
                     enumerate(mixed_up_board)]
        self.cols = [Row(col, c, False) for c, col in enumerate(zip(*self.rows))]
        self.board = {'rows': self.rows, 'cols': self.cols}

        # DEPREC: FOR DEBUG ONLY: CHECK METHOD
        self.shape = len(solved_board), len(solved_board[0])
        print(self)
        self.nodes = {node.position: node for node in chain(*self.rows)}
        self.solved_board = solved_board

    def __repr__(self):
        return '\n'.join([' '.join([str(val) for val in row]) for row in self.rows])

    def _liftshift(self, value):
        """first stage solving algorithm"""
        i, j = Node.current[value]
        r, c = Node.target[value]

        # (0) correct row & column
        if (i, j) == (r, c):
            return None

        # (1) correct row
        elif i == r and j != c:
            self.cols[j].rowshift(1)
            self.cols[c].rowshift(1)
            self.rows[r - 1].rowshift(
                min([j + len(self.rows[0]) - c, c - j], key=abs))  # potentially just set default shift right
            self.cols[j].rowshift(-1)
            self.cols[c].rowshift(-1)

        # (2) correct column
        elif i != r and j == c:
            self.rows[j].rowshift(-1)
            self.cols[c].rowshift(r - i)  # lift up
            self.rows[j].rowshift(1)
            self.cols[c].rowshift(i - r)  # lift down

        # (3) neither
        else:
            self.cols[c].rowshift(i - r)
            self.rows[i].rowshift(
                min([j + len(self.rows[0]) - c, c - j], key=abs))
            self.cols[c].rowshift(r-i)

    def _restore_order(self, start):
        """second stage solving algorithm"""
        pass

    def solve(self):
        """Your task: return a List of moves that will transform the unsolved
        grid into the solved one. All values of the scrambled and unscrambled
        grids will be unique! Moves will be 2 character long Strings"""

        # 1st stage (solving all but the first row)
        # ordered valued from low right until first row
        # CONSIDER sorting first to penultimate
        for value in [val for row in reversed(self.solved_board[1:]) for val in row]:
            self._liftshift(value)  # value = 'Z'
            # FIXME: if no shift or single shift is requred, extend is falty!

        # 2nd stage (solving the first row, starting at value 2)
        self._restore_order(2)  # fixme actually self.solved_board[0][1]

        # optional 3rd stage (a complete repeat of 2nd stage, starting at value 1)
        self._restore_order(2)  # fixme actually self.solved_board[0][0]

        if self != self.solved_board:  # unsolvable  # FIXME: self must be joined to nested list format of solved_board
            return None
        else:
            return Row.Solution

    # DEPREC: DEBUG METHODS: REMOVE WHEN SUBMITTING ----------------------------
    def shift(self, direction):
        """Primary method to play the game (change the state of board)
        :param direction: string such as L0, R1, D1, U2
        where L & R refer to rowshifts and D & U to column shifts.
        Integer refers to the respective row / column to be shifted"""
        direct, pos = tuple(direction)
        board = self.board[self.perspective[direct]]
        board[int(pos)].rowshift(direction=self.direct[direct])

        print(self)

    def debug_col_repr(self):  # DEPREC to print the columns (primarily debug method)
        print('\n'.join([' '.join([str(val) for val in row]) for row in self.cols]))

    def debug_check(self, moves):  # Deprec: Debug only
        for move in moves:
            self.shift(move)

        board = [[self.nodes[(r, c)].value for c in range(len(self.rows[0]))]
                 for r in range(len(self.rows))]

        return board == self.solved_board

    def debug_shuffle(self, number):  # Deprec: Debug only
        """method to create random tests"""
        from random import randint
        pass


if __name__ == '__main__':
    def board(str):
        return [list(row) for row in str.split('\n')]


    def run_test(start, end, unsolvable):

        # print_info(board(start), board(end))
        moves = loopover(board(start), board(end))
        if unsolvable:
            assert moves is None  # 'Unsolvable configuration

        else:
            assert Cyclic_shift(start, end).debug_check(moves) == True
            # TODO write check function!


    c = Cyclic_shift(board('ACDBE\nFGHIJ\nKLMNO\nPQRST'),
                     board('ABCDE\nFGHIJ\nKLMNO\nPQRST'))

    # c.shift('L0')
    # c.shift('U0')
    print()

    # # @test.it('Test 2x2 (1)')
    # run_test('12\n34', '12\n34', False)

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
    # set('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY') -set('WCMDJ\nORFBA\nKNGLY\nPHVSE\nTXQUI') == set()
    # same for vice versa, so the configuration is the problem!
    run_test('WCMDJ\nORFBA\nKNGLY\nPHVSE\nTXQUI',
             'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', True)

    # @test.it('Test 6x6')
    run_test('WCMDJ0\nORFBA1\nKNGLY2\nPHVSE3\nTXQUI4\nZ56789',
             'ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789', False)
