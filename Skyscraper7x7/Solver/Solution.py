class Solution:
    def __init__(self, boardsize):
        """The pure intent of this class is to sample problems"""
        self.boardsize = boardsize
        self.__board = self.sample_board(boardsize)
        self.clues = self.parse_clues_from_board(self.__board)

    def sample_board(self, problemsize):
        # TODO sample one permutation & and make use of updates (particularly StrategyStack)
        #  -> wasnt there a non informative clue? in this case, simply sample some tuple clue and make all others
        #  unifnormative - using the update strategies, the applicable tuples remain.
        #  now sample another. repeat. if there is no solution available, start again? or make use of stack?
        #  further, using only a fraction of the available clue information may indicate multiple solutions
        #  there are two options
        #   1) ensure that only one solution is available (hard) - requires checking all possible choices in
        #       StrategyStack - that is after given a clue and the CrossSolving strategy is applied.
        #   2) check a potential solution provided by any solver for visability - and return true,
        #       if the provided solution is in accordance with the clues and that each row & col is
        #       a valid permutation of the set of range(1, board.probsize +1). Jointly these two criteria should
        #       guarantee the correctness of a board.
        return None

    @staticmethod
    def find_row_clues(b):
        """
        :param b: list of lists!
        """
        row_clues = list()
        for row in b:
            front = board._visible(row)
            back = board._visible(tuple(reversed(row)))

            row_clues.append((front, back))
        return row_clues

    @staticmethod
    def parse_clues_from_board(b):
        """
        :param b: list of lists
        :return:
        """
        row_clues = Solution.find_row_clues(b)
        col_clues = Solution.find_row_clues(list(zip(*b)))
        return [*[clue[0] for clue in col_clues],
                *[clue[1] for clue in row_clues],
                *[clue[1] for clue in reversed(col_clues)],
                *[clue[0] for clue in reversed(row_clues)]]

    @staticmethod
    def parse_clues_from_board(board):
        """

        :param board: Skyscraper instance
        :return:
        """

        b = [list(board.downtown_row[i][0]) for i in range(board.probsize)]
        row_clues = Solution.find_row_clues(b)
        col_clues = Solution.find_row_clues(list(zip(*b)))

        # create a single line from the row & column clues.
        # by convention, the order is top, right, bottom, left
        # TODO carefull: different problemsizes return either tuple or list
        return [*[clue[0] for clue in col_clues],
                *[clue[1] for clue in row_clues],
                *[clue[1] for clue in reversed(col_clues)],
                *[clue[0] for clue in reversed(row_clues)]]

    @staticmethod
    def check_a_valid_solution(board, original_clue):
        """check if the proposed board - when interpreted for visibility matches the
        (possibly incomplete) original_clue. also ensures that all rows and columns are a 
        set of range(1, board.probsize +1) and the board is thereby a valid cityblock."""
        if not Solution.check_valid_board(board):
            return False

        b = [list(board.downtown_row[i][0]) for i in range(board.probsize)]
        interpreted = Solution.parse_clues_from_board(board)
        return all([True if o == i or o == 0 else False for o, i in zip(original_clue, interpreted)])

    def check_valid_board(board):
        """Debug method: check that all rows and columns are a
        set of range(1, board.probsize +1) and the board is thereby a valid cityblock."""
        b = [list(board.downtown_row[i][0]) for i in range(board.probsize)]
        numbers = set(range(1, board.probsize + 1))
        return all([set(row) == numbers for row in b]) and \
               all([set(col) == numbers for col in zip(*b)])


if __name__ == '__main__':
    from Skyscraper7x7.Solver.Solver import Skyscraper

    # (0) check the intpreted clue is the same as the kata's clue
    assert Solution.parse_clues_from_board(((3, 4, 2, 1), (1, 2, 3, 4), (2, 1, 4, 3), (4, 3, 1, 2))) == \
           [2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2]

    # (1) check the original board is obtainable from the parsed clue
    board = [[2, 1, 4, 3],
             [3, 4, 1, 2],
             [4, 2, 3, 1],
             [1, 3, 2, 4]]
    clue = Solution.parse_clues_from_board(board)

    board = tuple(tuple(row) for row in board)  # conversion to meet kata's expectation
    assert Skyscraper(clue).solve() == board

    # (2) Check kata's incomplete clue matches the board (the brovided board is
    # a valid solution given the clue)
    # CAREFULL: if cannot assert: the kata provided 0's
    interpreted = Solution.parse_clues_from_Lists(((5, 6, 1, 4, 3, 2),
                                                   (4, 1, 3, 2, 6, 5),
                                                   (2, 3, 6, 1, 5, 4),
                                                   (6, 5, 4, 3, 2, 1),
                                                   (1, 2, 5, 6, 4, 3),
                                                   (3, 4, 2, 5, 1, 6)))

    # interpreted = [2, 1, 3, 2, 2, 3, 4, 2, 3, 6, 3, 1, 1, 4, 2, 3, 3, 2, 4, 4, 1, 3, 2, 2]
    originalclu = [0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0]

    # check that the original Clue with incomplete information matches
    # the intrepreted clue from the solution's board (which has complete info)
    assert all([True if o == i or o == 0 else False for o, i in zip(originalclu, interpreted)])
