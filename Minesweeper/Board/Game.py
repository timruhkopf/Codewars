import sys

from .Node import Node
from ..Strategies import Strategy_Superset, Strategy_Endgame

# TODO reduce Recursion depth: unnecessary communication?
sys.setrecursionlimit(10 ** 6)


class Game:
    def __init__(self, board, n, context=None):
        """
        Playable Minesweeper board.
        :param board: List of lists of str. only '?' (character for unkown) or '0's.
        :param n: number of bombs
        :context: Optional Game_from_solved instance, that hides the solution.
        Game.open calls are redirected to Game_from_solved.open, that can despite
        privacy of the solved board reveal positions of the board.
        This way, Game is truly ignorant of the solution.
        """
        self.remain_bomb = n
        self.context = context
        self.dim = len(board), len(board[0])  # used by Node.find_neighbours

        # instantiate the communication network with their clues
        # do not invoke communication yet by setting state property!
        tuples = [(i, j) for i in range(self.dim[0]) for j in range(self.dim[1])]
        self.clues = {(r, c): Node(position=(r, c), clue='?', context=self)
                      for r, c in tuples}

        self.zeros = set((r, c) for r, c in tuples if board[r][c] == '0')
        # to make board playable by user: display which positions are 0s
        # for (r, c), node in self.clues.items():
        #     node._clue = board[r][c]

        # setting up the neighbourhood structure
        for node in self.clues.values():
            node.neighb_inst = set(self.clues[k] for k in node.neighbours)
            q = node.neighb_inst.copy()  # fixme. can copy be removed?
            node.questionmarks = set(p for p in q if p.clue == '?')

    def __repr__(self):
        return '\n'.join([' '.join(row) for row in self.board])

    def open(self, r, c):
        """
        inquire a position's true value from the solution (context object)
        :param r: int. row index that is to be opened
        :param c: int. column index that is to be opened
        :return: None. places new clue on board and removes the instance
        from its neighbours question marks.
        """
        if self.context is not None:
            value = int(self.context.open(r, c))
        else:
            value = open(r, c)

        node = self.clues[(r, c)]
        for n in node.neighb_inst:
            n.questionmarks.discard(node)

        node.clue = value

    def mark_bomb(self, bombs):
        """
        mark the bombs on the board and communicate them to their neighbours
        :param bombs: list of node instances, that were identified as bomb
        """
        while bool(bombs):
            b = bombs.pop()
            if b._clue == '?':  # not opened yet: check for statesafety
                # TODO exclude bombs entirely after spreading their info?
                #  to reduce recursion amount

                # (0) inform board
                b._clue = 'x'
                self.remain_bomb -= 1

                # (1) inform neighbours about being a bomb
                # not activating state setter yet! statesafety!
                for n in b.neighb_inst:
                    n._state -= 1
                    if b in n.questionmarks:
                        n.questionmarks.discard(b)

                # (2) Invoke recursion in statesafe enfiroment
                # let each neighbour check if the updated state
                # now contains info - either being 0 or all ? are bombs.
                for n in b.neighb_inst:
                    n.state = n._state

    def solve(self):
        # (0) open known zeros and use recursive communication on them only once
        # note how self.zeros can be empty after a single open call, if all zeros are
        # recursively connected & opened. this avoids opening the same 0 twice
        while bool(self.zeros):
            zero = self.zeros.pop()
            self.open(*zero)
            placedzeros = set(n.position for n in self.clues.values() if n.clue == 0)
            self.zeros.difference_update(placedzeros)

        # (1) find sets of nodes, that are jointly informative
        Strategy_Superset.execute(self)

        # (2) check if Superset was sufficient to solve
        Strategy_Endgame.simple(self)

        # (3) Endgame logic based on number of bombs.
        if bool(self.remain_bomb) and self.remain_bomb <= 3:
            Strategy_Endgame.sequential_combinations(self)

        # remaining ambiguity? --> Unsolvable
        if bool([inst._clue for inst in self.clues.values() if inst._clue == '?']):
            return '?'
        else:
            return self.board

    # Debug display methods. ---------------------------------------------------
    @property
    def board(self):
        return [[str(self.clues[(r, c)].clue) for c in range(self.dim[1])]
                for r in range(self.dim[0])]

    @property
    def state_map(self):
        state_board = [[str(self.clues[(r, c)].state) for c in range(self.dim[1])]
                       for r in range(self.dim[0])]
        print('\n'.join([' '.join(row) for row in state_board]))

    @property
    def q_map(self):
        state_board = [[str(len(self.clues[(r, c)].questionmarks))
                        if self.clues[(r, c)].clue != '?' else '*'
                        for c in range(self.dim[1])]
                       for r in range(self.dim[0])]
        print('\n'.join([' '.join(row) for row in state_board]))
