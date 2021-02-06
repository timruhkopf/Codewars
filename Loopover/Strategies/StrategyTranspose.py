class StrategyTranspose:
    def execute_strategy(board):
        """"""
        # TODO less complicated way (and readable) for transpose algo  would be to initialize the algo on the
        #  transposed board and translate the solution
        #  always choose row/column major by the dimension (row/column) that
        #  has an even length (as this dim is guaranteed to have a proper sorting graph)
        #  UNSOLVABLES in this scenario are those, that have uneven in both dim
        #  and after solving one up to toprow , the transpose solve is also faulty.

        # TODO board.solve has to decide when to use Transpose.
        #  Be carefull not to create a loop! use a decorator on solve to determine
        #  the row / column major? Here: call wrapped function!

        solved_board = board.solved_board
        mixed_board = board.mixed_up_board

        board.__init__([list(col) for col in zip(*mixed_board)])
        board.solve([list(col) for col in zip(*solved_board)])
        solution = board.solution

        # reverse transpose (to make it look like it was the same board afterall
        board.__init__([list(col) for col in zip(*board.toList())])
        board.solved_board = solved_board

        board.solution = StrategyTranspose.translate_solution(solution)

    @staticmethod
    def translate_solution(solution):
        """Since the board was solved for its Transpose (columnmajor), the solution
        cannot be reproduced in its original board version (rowmajor).
        As consequence the solution must be translated."""

        translation = {'L': 'U', 'R': 'D', 'U': 'L', 'D': 'R'}
        return [translation[letter] + ind for letter, ind in solution]
