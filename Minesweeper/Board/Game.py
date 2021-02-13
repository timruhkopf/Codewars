from .Node import Node


class Game:
    def __init__(self, board, n, context=None):
        """
        Playable Minesweeper board.
        :param board: List of lists of str. only '?' (character for unkown) or '0's.
        :param n: number of bombs
        :param context: Optional Game_from_solved instance, that hides the solution.
        Game.open calls are redirected to Game_from_solved.open, that can despite
        privacy of the solved board reveal positions of the board.
        This way, Game is truly ignorant of the solution.
        """
        self.b = board  # deprec
        self.remain_bomb = n
        # TODO refactor Node.context & Game.context to more meaningful attributes
        self.context = context
        self.dim = len(board), len(board[0])  # used by Node.find_neighbours

        # instantiate the communication network with their clues
        # do not invoke communication yet by setting state property!
        tuples = [(i, j) for i in range(self.dim[0]) for j in range(self.dim[1])]
        self.clues = {(r, c): Node(position=(r, c), context=self)
                      for r, c in tuples}

        # to make board playable by user: display which positions are 0s
        # todo make this clean: zeroind has a dependency to this
        # for (r, c), node in self.clues.items():
        #     node._clue = board[r][c]
        self.zeroind = [(r, c) for r, row in enumerate(board) for c, v in enumerate(row) if v == '0']

        # setting up the neighbourhood structure
        for node in self.clues.values():
            node.neighb_inst = set(self.clues[k] for k in node.neighbours)
            q = node.neighb_inst.copy()  # fixme. can copy be removed?
            node.questionmarks = set(p for p in q if p.clue == '?')

    def __repr__(self):
        return '\n'.join([' '.join(row) for row in self.board])

    @property
    def board(self):
        return [[str(self.clues[(r, c)].clue) for c in range(self.dim[1])] for r in range(self.dim[0])]

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

    def open(self, r, c):
        """
        inquire a position's true value from the solution (context object)
        :param r: int. row index that is to be opened
        :param c: int. column index that is to be opened
        :return: None. places new clue on board and removes the instance
        from its neighbours question marks.
        """
        value = int(self.context.open(r, c))
        self.b[r][c] = str(value)  # deprec
        return value

    # def open(self,r, c):
    #     # the kata requires to call open plainly - and overwrites the open keyword!
    #     return open(r,c)
