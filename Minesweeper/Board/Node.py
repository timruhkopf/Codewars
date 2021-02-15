class Node:

    def __init__(self, position, clue='?', context=None):
        self.context = context

        self.position = position
        self._clue = clue
        self._state = 0

        neighbours = self._find_neighbours(*position)
        self.neighbours = neighbours
        self.neighb_inst = set()
        self.questionmarks = set()

    def __repr__(self):  # for debugging only
        # return str(self._clue)
        return str((self.position, 'clue:', self._clue, 'state:', self.state))

    def __str__(self):
        return str(self._clue)

    def __hash__(self):  # to support in
        return hash(self.position)

    def __eq__(self, other):  # to support in
        return self.position == other.position

    def isneighb(self, other):
        """
        checks if two Nodes are Neighbours.
        convenience method for superset logic.
        :param other: other Node instance
        :return: boolean
        """
        return other in self.neighb_inst

    @property
    def clue(self):
        return self._clue

    @clue.setter
    def clue(self, value):
        # TODO check if body can be moved to context.open & remove property
        # called at open of this position.
        # at opening --> statechange ? to CLUE. here prior information
        # already contained in ?: self.state has to be added.
        self._clue = value
        self.state = value + self.state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        # open all questionmarks of a Clue instance by its state hitting 0
        if value == 0:
            # open all ?
            self._state = 0
            while bool(self.questionmarks):  # while to account for changes during recursion.
                q = self.questionmarks.pop()
                self.context.open(*q.position)

            # check if any neighb knows  it's ?s are bombs.
            for n in self.neighb_inst:
                if n.state == len(n.questionmarks):
                    self.context.mark_bomb(bombs=self.questionmarks)

        # default case, setting the received value and check if my ? are all bombs
        #  --> update state of a ? and a Clue instance
        else:
            self._state = value
            if self.state == len(self.questionmarks):
                self.context.mark_bomb(bombs=self.questionmarks)

    def _find_neighbours(self, r, c):
        """
        :returns the set of all neighbours (excluding self's position).
        all of them are bound checked"""
        cond = lambda r, c: 0 <= r < self.context.dim[0] and 0 <= c < self.context.dim[1]
        kernel = (-1, 0, 1)
        neighb = set((r + i, c + j) for i in kernel for j in kernel
                     if cond(r + i, c + j) and cond(r + i, c + j))
        neighb.discard((r, c))
        return neighb
