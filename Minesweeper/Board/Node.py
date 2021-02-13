from ..Strategies.CommunicationStates import State_Q


class Node:

    def __init__(self, position, context):
        self.position = position
        self.context = context
        self._state = 0
        self._clue = '?'  # deprec but used for game. init

        # set up basic neighb. structure without filling.
        # context fills relations after all nodes are created
        neighbours = self._find_neighbours(position, context.dim)
        self.neighbours = neighbours
        self.neighb_inst = set()  # other position instances
        self.questionmarks = set()

        self.STATE = State_Q(node=self)

    @property
    def clue(self):
        return self.STATE._clue

    @property
    def state(self):
        return self.STATE._state

    def __repr__(self):  # for debugging only
        # return str(self.clue)
        return str((self.position, 'clue:', self.clue, 'state:', self.state))

    def __str__(self):
        return str(self.clue)

    def __hash__(self):  # to support in
        return hash(self.position)

    def __eq__(self, other):  # to support in
        return self.position == other.position

    def isneighb(self, other):  # Deprec
        return other in self.neighb_inst

    @staticmethod
    def _find_neighbours(position, dim):
        """
        :param position: tuple. row, column index.
        :param dim: tuple: row, column dimension.
        :return: set of all neighbour indicies (excluding self's position).
        all of them are bound checked
        """
        # todo update doc
        # todo make a lazy method? / lazy property?
        r, c = position
        cond = lambda r, c: 0 <= r < dim[0] and 0 <= c < dim[1]
        kernel = (-1, 0, 1)
        neighb = set((r + i, c + j) for i in kernel for j in kernel
                     if cond(r + i, c + j) and cond(r + i, c + j))
        neighb.discard((r, c))
        return neighb
