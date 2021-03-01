from .Board.Game import Game


def board(strboard):
    return [[v for v in row] for row in strboard.strip().replace(' ', '').split('\n')]


def solve_mine(scrambled, nbombs):
    """
    The kata's required interface
    :param scrambled:
    :param nbombs:
    :return: the solved board
    """
    return Game(board=scrambled, n=nbombs).solve()