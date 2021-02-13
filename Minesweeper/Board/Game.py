import sys

from .Node import Node

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
        self.clues = {(r, c): Node(position=(r, c), clue=board[r][c], context=self)
                      for r, c in tuples}

        # # to make board playable by user: display which positions are 0s
        # for (r, c), node in self.clues.items():
        #     node.clue = board[r][c]

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
        value = int(self.context.open(r, c))
        node = self.clues[(r, c)]

        for n in node.neighb_inst:
            n.questionmarks.discard(node)

        node.clue = value

    def solve(self):
        # (0) open known zeros and use recursive communication
        zeros = [n.position for n in self.clues.values() if n.clue == '0']
        for ind in zeros:
            self.open(*ind)

        # (1) exactly one bomb in questionmarks logic
        # Strategy_Superset.execute(self)
        #
        # (2) check if Superset was sufficient
        # remain_q = [_ for _ in self.clues.values() if _._clue == '?']
        # if self.remain_bomb == len(remain_q):
        #     Position.bombastic(remain_q)  # FIXME bombastic
        # elif self.remain_bomb == 0 and len(remain_q) != 0:
        #     for _ in remain_q:
        #         self.open(*_.position)
        #
        # # (3) Endgame logic based on number of bombs.
        # if bool(self.remain_bomb) and self.remain_bomb <= 3:
        #     Strategy_Endgame.execute(self)
        #
        # # remaining ambiguity? --> Unsolvable
        # if bool([inst._clue for inst in self.clues.values() if inst._clue == '?']):
        #     return '?'
        # else:
        #     return self.board

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
