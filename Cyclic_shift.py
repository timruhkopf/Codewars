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
    Solution = list() # allows both row and column instances to comunicate
    #  but is a sensitive area in parallel computing!
    direct = {True: ('L', 'R'), False: ('U', 'D')}   # fixme potentially U D are in wrong order!

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
        return [self.direct[self.row][direction > 0] + self.ind] * abs(direction)


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
        Row.Solution = list() # overwrite last cyclic_shift instance's solution
        self.rows = [Row([Node((r, c), val) for c, val in enumerate(row)], r, True) for r, row in
                     enumerate(mixed_up_board)]
        self.cols = [Row(col, c, False) for c, col in enumerate(zip(*reversed(self.rows)))]

        self.rdim, self.cdim = len(self.rows[0]), len(self.cols[0])
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

        # (0) correct row & column
        if (i, j) == (r, c):
            return None

        if DEBUG:
            print('Intent:', value, '--->', self.nodes[Node.target[value]].value)
            prev_sol = len(Row.Solution)

        # (1) correct row
        if i == r and j != c:
            self.cols[j].shift(1)
            self.cols[c].shift(1)
            self.rows[r - 1].shift(min([-(j + self.rdim - c), c - j], key=abs))  # FIXME: this one is faulty!!
            self.cols[j].shift(-1)
            self.cols[c].shift(-1)

        # (2) correct column
        elif j == c and i != r:
            self.rows[i].shift(-1)
            self.cols[c].shift(-(i - r))  # lift up
            self.rows[i].shift(1)
            self.cols[c].shift(i - r)  # lift down

        # (3) neither
        else:
            self.cols[c].shift(-(i - r))
            self.rows[i].shift(min([-(j + self.rdim + 1 - c), c - j], key=abs))
            self.cols[c].shift(i - r)

        if DEBUG:
            print('Suggested Path:', Row.Solution[prev_sol:])
            print(self)
            print('\n')

    def find_misplaced(self):
        """:return dict: key, value indicates key ---> value: the value indicates
         the current occupant of the position, where key must be placed."""
        # original variant
        # _, current = Node.current[ref]
        # self.rows[0].shift(-current)
        # misplaced = {x: y for x, y in
        #              zip(self.solved_board[0], [v.value for v in self.rows[0]]) if x != y}

        # new variant
        # TODO IDEA HERE: make the ref value match the position of the solved board
        # THEN check which are not aligned. (the number of changes required likely changes, if any values are
        # consecutively soreted!)
        for ref in self.solved_board[0]:

            # ref = 'E'  # CONSIDER: with rowlen = 5, only those ref that cause uneven no. (here exacly 3) solve
            #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            _, c = Node.current[ref]
            _, t = Node.target[ref]

            self.rows[0].shift(min(-(c - t), self.rdim - c + t))
            # d = deque(maxlen=len(self.solved_board[0]))
            # d.extend([n.value for n in self.rows[0]])
            #
            # _, c = d.(ref)
            # _, t = Node.target[ref]
            #
            # d.rotate(min(-(c - t), self.rdim - c + t))

            print('\n', [n.value for n in self.rows[0]],
                  '\n', self.solved_board[0])
            misplaced = {x: y for x, y in
                         zip(self.solved_board[0], [v.value for v in self.rows[0]]) if x != y}

            print(ref, ':', len(misplaced), '\n\n')

            if len(misplaced) % 2 != 0:
                return misplaced, ref

        # NO solution with uneven number of steps was found
        return {}, self.solved_board[0][0]

    def _sort_toprow(self):  # , direct=-1):
        """second stage solving algorithm, a directed graph approach"""
        misplaced, ref = self.find_misplaced()
        if not bool(misplaced):
            return None  # _sort_toprow not needed
        start, target = misplaced.popitem()

        # direct = -1

        def initalisation(start):
            # align with reference - to find correct wild_occupies
            _, r = Node.current[ref]
            _, t = Node.target[ref]
            self.rows[0].shift(t - r)

            _, s = Node.current[start]
            wild_occupies = self.solved_board[0][s]  # FIXME: must depend on the reference!
            self.rows[0].shift(min(-s, self.rdim - s, key=abs))
            self.cols[0].shift(-1)
            wildcard = self.rows[0][0].value
            misplaced[wild_occupies] = wildcard  # FIXME: can add a path if
            i = 0  # {-1: 0, 1: 1}[direct]
            return wildcard, i

        wildcard, i = initalisation(start)

        while start != target:
            print(self, '\n', start, '-->', target)
            _, t = Node.current[target]
            self.rows[0].shift(min(-t, self.rdim - t, key=abs))
            self.cols[0].shift([1, -1][i % 2])

            start = target
            i += 1

            if target == wildcard:
                if bool(misplaced):
                    start, target = misplaced.popitem()
                    # direct = -1
                    wildcard, i = initalisation(start)  # fixme: if twice in a row a wild card is hit, this fails

            elif len(misplaced) > 0:
                target = misplaced.pop(start)

        _, t = Node.current[self.solved_board[0][0]]
        self.rows[0].shift(-t)
        print(self, '\n')

    def solve(self):
        """Your task: return a List of moves that will transform the unsolved
        grid into the solved one. All values of the scrambled and unscrambled
        grids will be unique! Moves will be 2 character long Strings"""

        # 1st stage (solving all but the first row)
        # ordered values from low left until first row
        # CONSIDER sorting first to penultimate
        for value in [val for row in reversed(self.solved_board[1:]) for val in reversed(row)]:
            self._liftshift(value)

        # # 2nd stage (solving the first row, starting at value 2)
        # if self.solved_board[0] != [str(val) for val in self.rows[0]]:
        #     self._restore_order(ref=self.solved_board[0][0])
        # else: # already solved board
        #     return Row.Solution
        #
        # # optional 3rd stage (a complete repeat of 2nd stage, starting at value 1)
        # if self.solved_board[:2] != [[str(val) for val in row] for row in self.rows[:2]]:
        #     self.second_order()

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

    def debug_check(self, moves):
        for move in moves:
            self.shift(move)
            print(self)
            print('\n')

        return all([self.solved_board[r] == [str(val) for val in self.rows[r]]  for r in range(self.cdim)])

    def debug_shuffle(self, steps):  # Deprec: Debug only
        """method to create random tests"""
        from random import sample

        rows = [self.rows, self.cols]
        direction = [1, -1]

        for i in range(steps):
            row = sample(rows)  # row or column
            r = sample(row)  # which particular?
            r.shift(sample(direction))

        scrambled = ""

        return scrambled


if __name__ == '__main__':
    def board(str):
        return [list(row) for row in str.split('\n')]


    def run_test(start, end, unsolvable):

        # print_info(board(start), board(end))
        moves = loopover(board(start), board(end))
        if unsolvable:
            assert moves is None  # 'Unsolvable configuration

        else:
            moves = tuple(moves)
            assert Cyclic_shift(board(start), board(end)).debug_check(moves) == True


    # calibration test
    c = Cyclic_shift(board('ACDBE\nFGHIJ\nKLMNO\nPQRST'),
                     board('ABCDE\nFGHIJ\nKLMNO\nPQRST'))
    c.shift('L0')
    assert(Row.Solution[-1] == 'L0')
    c.shift('R0')
    assert(Row.Solution[-1] == 'R0')
    c.shift('D0')
    assert(Row.Solution[-1] == 'D0')
    c.shift('U0')
    assert(Row.Solution[-1] == 'U0')

    # TODO FIND MORE TESTS also of now working ones!!

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
