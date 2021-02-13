from .CommunicationStates import State_zero, State_Clue

from ..Util import board


# TODO refactor into Solver.solve() method


class StrategyOpenZero:
    def execute(game):
        # find all zeros and set their state to State_Clue: one after another
        # ToDO calculate zeroind

        zeroind = [(2, 2), (2, 3), (1, 3), (0, 3)]
        for z in zeroind:  # game.zeroind:  # fixme: single zero of a each zero group is enough!
            zero = game.clues[z]
            zero.STATE = State_zero(zero)


class StrategyZeroAnreiner:
    def execute(game):
        # INITIAL ZEROS

        # communicate the intial zero-Position's questionmarks to open
        # reducing the unneccessary recursion across zeros, by removing them altogether
        anreiner = set()
        for z in game.zeroind:
            zero = game.clues[z]

            anreiner.update(zero.questionmarks)
            # remove zero from any communication
            while bool(zero.questionmarks):
                n = zero.questionmarks.pop()
                n.questionmarks.discard(zero)
                n.neighb_inst.discard(zero)

        # for debug check, if the order of openening makes a difference (state safety)
        # from random import shuffle
        # anreiner = list(anreiner)
        # shuffle(anreiner)

        game.anreiner = anreiner
        for q in anreiner:
            q.STATE = State_Clue(q)
            # game.open(*q.position)
            # print('game:', game, '\n\n')
            # print('Q:', game.q_map, '\n\n')
            # print('state:', game.state_map, '\n\n')


if __name__ == '__main__':
    from ..Board.Game import Game
    from ..Board.Solution import Solution

    # result = """
    #       1 x x 1 0
    #       2 3 3 1 0
    #       1 x 1 0 0
    #       1 1 1 0 0
    #       0 0 0 0 0
    #       """

    result = """
    1 x 1 0
    1 2 1 0
    x 1 0 0
    """

    solution = Solution(board(result))

    m = Game(board=solution.covered_board, n=solution.n, context=solution)

    StrategyOpenZero.execute(m)

    # FIXME: (1,2) still has the zeros as questionmarks, the qs tend to not remove themselves
    m.clues[(1, 2)]
    # ((1, 2), 'clue:', 1, 'state:', 1)
    m.clues[(1, 2)].questionmarks
    # {((0, 1), 'clue:', '?', 'state:', 0), ((0, 3), 'clue:', 0, 'state:', 0), ((2, 3), 'clue:', 0, 'state:', 0), ((2, 2), 'clue:', 0, 'state:', 0), ((1, 3), 'clue:', 0, 'state:', 0)}

    # StrategyZeroAnreiner.execute(m)
