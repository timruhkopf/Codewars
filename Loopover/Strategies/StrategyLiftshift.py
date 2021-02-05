from ..Board.Row import Node


class StrategyLiftshift:
    def executeStrategy(board):
        for value in [val for row in reversed(board.solved_board[1:]) for val in reversed(row)]:
            StrategyLiftshift.liftshift(board, value)

    def liftshift(board, value):
        """first stage solving algorithm, solves all but the first row, with three
        minor algorithms, depending on the respective position to the target
        :param value: str. letter, that is to be moved to its target position."""
        i, j = Node.current[value]
        r, c = Node.target[value]

        # (0) correct row & column
        if (i, j) == (r, c):
            return None

        # (1) correct row
        if i == r and j != c:
            board.cols[j].shift(1)
            board.cols[c].shift(1)
            board.rows[r - 1].shift(board.rows[r - 1].shortest_shiftLR(j, c))
            board.cols[j].shift(-1)
            board.cols[c].shift(-1)

        # (2) correct column
        elif j == c and i != r:
            board.rows[i].shift(-1)
            board.cols[c].shift(-(i - r))  # lift up # CONSIDER: Room for improvment: cols[c].shortest_shiftLR(i, r)
            board.rows[i].shift(1)
            board.cols[c].shift(i - r)  # lift down  # CONSIDER: Room for improvment: cols[c].shortest_shiftLR(r, i)

        # (3) neither
        else:
            board.cols[c].shift(-(i - r))
            board.rows[i].shift(board.rows[i].shortest_shiftLR(j, c))
            board.cols[c].shift(i - r)
