class Debugbehaviour:
    # TODO Remove: this for submitting, but add to cyclic shift as playable
    #  methods for the board

    def shift(self, direction):
        """Primary method to play the game & checking the solution.
        It is not used in solving)

        :param direction: string such as L0, R1, D1, U2
        where L & R refer to rowshifts and D & U to column shifts.
        Integer refers to the respective row / column to be shifted"""
        direct, pos = tuple(direction)

        board = {'L': self.rows, 'R': self.rows, 'D': self.cols, 'U': self.cols}[direct]
        board[int(pos)].shift(direction=self.direct[direct])

    def shuffle(self, steps):
        """method to create random tests"""
        from random import sample

        for s in range(steps):
            direction = sample('LRUD', 1)[0]
            if direction in 'LR':
                stepsize = str(sample(range(self.cdim), 1)[0])
            else:
                stepsize = str(sample(range(self.rdim), 1)[0])

            self.shift(direction + stepsize)

        return '\n'.join([''.join([node.value for node in row]) for row in self.rows])

    def debug_check(self, moves, solved_board):
        for move in moves:
            self.shift(move)
            # print(self)
            # print('\n')

        return all([solved_board[r] == [str(val) for val in self.rows[r]] for r in range(self.cdim)])


class Context:
    # Default only for test cases, to initialise Row with no context
    solution = []


def board(strboard):
    return [list(row) for row in strboard.split('\n')]
