
class Debugbehaviour:
    # DEPREC: DEBUG METHODS: REMOVE WHEN SUBMITTING ----------------------------
    def shift(self, direction):
        """Primary method to play the game (change the state of board)
        :param direction: string such as L0, R1, D1, U2
        where L & R refer to rowshifts and D & U to column shifts.
        Integer refers to the respective row / column to be shifted"""
        direct, pos = tuple(direction)

        board = {'L': self.rows, 'R': self.rows, 'D': self.cols, 'U': self.cols}[direct]
        board[int(pos)].shift(direction=self.direct[direct])

        # print(self)

    def debug_check(self, moves, solved_board):
        # self.shape = len(self.mixed_up_board), len(self.mixed_up_board[0])
        # self.nodes = {node.position: node for node in chain(*self.rows)}

        for move in moves:
            self.shift(move)
            print(self)
            print('\n')

        return all([solved_board[r] == [str(val) for val in self.rows[r]] for r in range(self.cdim)])

    def shuffle(self, steps):
        """method to create random tests"""
        from random import sample

        for s in range(steps):
            direction = sample('LRUD', 1)[0]
            if direction in 'LR':
                stepsize = str(sample(range(self.cdim), 1)[0]) # TODO fix self.rdim & self.cdim
            else:
                stepsize = str(sample(range(self.rdim), 1)[0])

            self.shift(direction+stepsize)

        return '\n'.join([''.join([node.value for node in row]) for row in self.rows])


