from Skyscraper7x7.Solver import Skyscraper


class Solution:
    def __init__(self, boardsize):
        """The pure intent of this class is to sample problems"""
        self.boardsize = boardsize
        self.__board = self.sample_board(boardsize)
        self.clues = self.parse_clues_from_board(self.__board)

    def sample_board(self, problemsize):
        # TODO sample one permutation & and make use of updates
        #  -> wasnt there a non informative clue? in this case, simply sample some tuple clue and make all others
        #  unifnormative - using the update strategies, the applicable tuples remain.
        #  now sample another. repeat. if there is no solution available, start again? or make use of stack?
        return None

    @staticmethod
    def parse_clues_from_board(board):
        # use zip transpose & visability

        def find_row_clues(board):
            row_clues = list()
            for row in board:
                front = Skyscraper._visible(row)
                back = Skyscraper._visible(tuple(reversed(row)))

                row_clues.append((front, back))
            return row_clues

        row_clues = find_row_clues(board)
        col_clues = find_row_clues(list(zip(*board)))

        # create a single line from the row & column clues.
        # by convention, the order is top, right, bottom, left
        # TODO carefull: different problemsizes return either tuple or list
        return [*[clue[0] for clue in col_clues],
                *[clue[1] for clue in row_clues],
                *[clue[1] for clue in reversed(col_clues)],
                *[clue[0] for clue in reversed(row_clues)]]


if __name__ == '__main__':
    assert Solution.parse_clues_from_board(((3, 4, 2, 1), (1, 2, 3, 4), (2, 1, 4, 3), (4, 3, 1, 2))) == \
           [2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]

    # CAREFULL: if cannot assert: the kata provided 0's
    # assert Solution.parse_clues_from_board(((5, 6, 1, 4, 3, 2),
    #                                         (4, 1, 3, 2, 6, 5),
    #                                         (2, 3, 6, 1, 5, 4),
    #                                         (6, 5, 4, 3, 2, 1),
    #                                         (1, 2, 5, 6, 4, 3),
    #                                         (3, 4, 2, 5, 1, 6))) == \
    # [0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0]
    # [2, 1, 3, 2, 2, 3, 4, 2, 3, 6, 3, 1, 1, 4, 2, 3, 3, 2, 4, 4, 1, 3, 2, 2]
