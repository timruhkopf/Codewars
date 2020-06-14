from collections import deque
from itertools import chain, cycle

DEBUG = True


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

    def shift(self, direction):
        """:param direction: integer. value of integer indicates the number of
        repeated shifts. the sign indicates a left(-) or right(+) shift"""
        self.queue.extend([node.value for node in self])  # overwrites at each step the queue

        print(self)
        self.queue.rotate(direction)

        self.Solution.extend(self.direction_parser(direction))

        for node, v in zip(self, self.queue):
            node.value = v
            Node.current[v] = node.position  # still efficient as merely pointer
            # to immutable tuple is shared (no new tuple is created)

        print(self, self.direction_parser(direction))

    def direction_parser(self, direction):
        """:param direction: integer: number of shifts, left shift is negative, right positive"""
        return [self.direct[self.row][direction < 0] + self.ind] * abs(direction)


class Cyclic_shift:
    direct = {'L': -1, 'R': 1, 'D': 1, 'U': -1}
    perspective = {'L': 'rows', 'R': 'rows', 'D': 'cols', 'U': 'cols'}
    rdim, cdim = 0, 0

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

        self.rdim, self.cdim = len(self.rows[0]), len(self.rows[0])
        self.solved_board = solved_board

        # DEPREC: required for CHECK METHOD!
        if DEBUG:
            self.board = {'rows': self.rows, 'cols': self.cols}
            self.shape = len(solved_board), len(solved_board[0])
            print(self)
            print()
            self.nodes = {node.position: node for node in chain(*self.rows)}

    def __repr__(self):
        return '\n'.join([' '.join([str(val) for val in row]) for row in self.rows])

    def _liftshift(self, value):
        """first stage solving algorithm"""

        i, j = Node.current[value]
        r, c = Node.target[value]

        if DEBUG:
            print('Intent:', value, '--->', self.nodes[Node.target[value]].value)
            prev_sol = len(Row.Solution)

        # (0) correct row & column
        if (i, j) == (r, c):
            return None

        # (1) correct row
        elif i == r and j != c:
            self.cols[j].shift(-1)
            self.cols[c].shift(-1)
            self.rows[r - 1].shift(min([j + self.rdim - c, c - j], key=abs))
            self.cols[j].shift(1)
            self.cols[c].shift(1)

        # (2) correct column
        elif i != r and j == c:
            self.rows[i].shift(-1)
            self.cols[c].shift(i - r)  # lift up
            self.rows[i].shift(1)
            self.cols[c].shift(-(i - r))  # lift down

        # (3) neither
        else:
            self.cols[c].shift(i - r)
            self.rows[i].shift(min([j + self.rdim + 1 - c, c - j], key=abs))
            self.cols[c].shift(-(i - r))

    def _restore_order(self, ref, start=1):
        """second stage solving algorithm"""
        # generate all cyclic permutations of the target row for stopping criterion
        x = cycle(self.solved_board[0])
        cycs = list()
        for i in range(self.rdim):
            cycs.append([next(x) for i in self.solved_board[0]])
            next(x)

        # init of algo
        i, j = Node.current[self.solved_board[0][start]]  # starting value
        r, c = Node.target[self.solved_board[0][start]]  # target value
        self.rows[0].shift(-j)
        self.cols[0].shift(-1)

        counter = 0
        # while not any cyclic permutation of true state found
        while [str(val) for val in self.rows[0]] not in cycs:  # FIXME: this might go indefinet if not solvable!!!!
            print('\n')
            print(self)
            _, cc = Node.current[ref]
            c = cc + c % self.rdim - 1  # new target position, relative to reference:
            self.rows[0].shift(min([-c, self.rdim - c], key=abs))

            # next value we are looking for
            _, c = Node.target[self.rows[0][0].value]
            self.cols[0].shift([1, -1][counter % 2])  # alternating up and down
            counter += 1

        _, c = Node.current[self.solved_board[0][0]]
        self.rows[0].shift(min([-c, self.rdim - c], key=abs))
        print('\n')
        print(self)

    def second_order(self):
        """optional third stage solving algorithm"""
        for i in range(self.cdim):
            self.cols[0].shift(-1)
            self.rows[0].shift(-1)
            self.cols[0].shift(1)
            self.rows[0].shift(-1)

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
        self._restore_order(ref=self.solved_board[0][0])

        # optional 3rd stage (a complete repeat of 2nd stage, starting at value 1)
        if self.solved_board[:2] != [[str(val) for val in row] for row in self.rows[:2]]:
            self.second_order()

        if self.solved_board != [[str(val) for val in row] for row in self.rows]:  # unsolvable
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
        board[int(pos)].shift(direction=self.direct[direct])

        print(self)

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


    # c = Cyclic_shift(board('ACDBE\nFGHIJ\nKLMNO\nPQRST'),
    #                  board('ABCDE\nFGHIJ\nKLMNO\nPQRST'))

    # c.shift('L0')
    # c.shift('U0')
    print()

    # # @test.it('Test 2x2 (1)')
    # run_test('12\n34', '12\n34', False)

    # @test.it('Test 2x2 (2)')
    # run_test('42\n31', '12\n34', False)

    # @test.it('Test 4x5')
    # run_test('ACDBE\nFGHIJ\nKLMNO\nPQRST',
    #          'ABCDE\nFGHIJ\nKLMNO\nPQRST', False)

    # @test.it('Test 5x5 (1)')
    # run_test('ACDBE\nFGHIJ\nKLMNO\nPQRST\nUVWXY',
    #          'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

    # @test.it('Test 5x5 (2)')

    # run_test('ABCDE\nKGHIJ\nPLMNO\nFQRST\nUVWXY',
    #          'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

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
