from .Game import Game


class Solution:
    def __init__(self, solved_board=None):
        """
        Interface for Minesweeper, that hides the true board from the playable board
        but allows to open specific positions via Game_from_solved_open.
        This class comes in handy in two ways: Debug interface - the Game class is truly
        ignorant of the solution and second, its sample_board method creates
        new playable boards.

        Instances to this class carry the solution of a board privately and translate
        it to a problem, that can be passed to Game class for solving.

        :param solved_board: list of lists. nested lists all of same length.
        nested list contains strings from '?', indicating unkown positions,
        'x': indicating bombs and string numbers '1' to '8' indicating the number
        of bombs in the neighbourhood of this position
        """
        if solved_board is not None:
            self.__solved_board = solved_board  # private attribute
            self.n = solved_board.count('x')
            self.covered_board = [['?' if v != '0' else v for v in row] for row in solved_board]
        else:
            self.sample_board(nbombs=10, dim=(10, 10))

    def __repr__(self):
        return '\n'.join(' '.join(row) for row in self.covered_board)

    def open(self, r, c):
        """
        Access the positions from the private attribute self.__solved_board from
        out of scope.
        :param r: int. row index that is to be opened
        :param c: int. column index that is to be opened
        :return: str. clue at the inquired position
        :raises: Value Error, if the inquired position is occupied by a bomb
        """
        value = self.__solved_board[r][c]
        if value == 'x':
            raise ValueError('What a bummer.')

        return value

    def sample_board(self, nbombs, dim):
        """

        :param nbombs: int. number of bombs placed on the board
        :param dim: tuple: rowdimension, column dimension of the board
        :return: List of list of str, containing only '?' and 'x'.
        Reinstantiates the instance with the new private self.__solved_board
        and the new self.covered_board
        """
        from random import sample
        self.n = nbombs

        bombs = sample([(i, j) for i in range(dim[0]) for j in range(dim[1])], nbombs)
        new_board = [['x' if (r, c) in bombs else '?' for r in range(dim[0])] for c in range(dim[1])]

        # use the Positions of game to easily count the bombs around it
        game = Game(new_board, n=nbombs, context=None)
        for position in game.clues.values():
            if position.clue != 'x':
                position._state = [n._clue for n in position.neighb_inst].count('x')
                position._clue = position._state
                r, c = position.position
                new_board[r][c] = str(position._state)

        # ensure there is at least one zero
        if not any(bool(row.count('0')) for row in new_board):
            self.sample_board(nbombs, dim)
        else:
            self.__init__(solved_board=new_board)
            return new_board


if __name__ == '__main__':
    from ..Util import board

    gamemap = """
       ? ? ? ? 0 0 0
       ? ? ? ? 0 ? ?
       ? ? ? 0 0 ? ?
       ? ? ? 0 0 ? ?
       0 ? ? ? 0 0 0
       0 ? ? ? 0 0 0
       0 ? ? ? 0 ? ?
       0 0 0 0 0 ? ?
       0 0 0 0 0 ? ?
       """.replace(' ', '')
    result = """
       1 x x 1 0 0 0
       2 3 3 1 0 1 1
       1 x 1 0 0 1 x
       1 1 1 0 0 1 1
       0 1 1 1 0 0 0
       0 1 x 1 0 0 0
       0 1 1 1 0 1 1
       0 0 0 0 0 1 x
       0 0 0 0 0 1 1
       """.replace(' ', '')

    # test open from context works
    result_board = Solution(board(result))
    m = Game(board(gamemap), n=result.count('x'), context=result_board)
    m.open(0, 0)
    print(m)

    # sample a board:
    result_board = Solution()
    result_board.sample_board(10, dim=(5, 7))

    # TODO write test case with new interface!
