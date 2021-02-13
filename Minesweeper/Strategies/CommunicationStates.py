class State_Nonresponsive:
    def discardQ(self, other):
        return None


class STATE:
    """Abstract class for debugging: """

    def __repr__(self):
        return self.node.__repr__()

    @property
    def board(self):
        print(self.node.context)

    def __init__(self):
        # first time execution
        pass

    def discardQ(self):
        # what to do if questionmarks are removed from self.node
        pass


class State_zero(STATE, State_Nonresponsive):
    _state = 0
    _clue = '0'

    def __init__(self, node):
        """

        :param node: a Node instance: the reference to the object, that is in
        the State_zero
        """
        # Consider pass only if anreiner strategy!
        self.node = node
        self._clue = 0

        # inform all neighb, that we no longer are a questionmark
        for n in self.node.neighb_inst:
            n.STATE.discardQ(self.node)

        # open all its questionmarks
        while bool(self.node.questionmarks):
            n = self.node.questionmarks.pop()
            if isinstance(n.STATE, State_Q):  # prevents opening already open zeros
                n.STATE = State_Clue(n, n._state)

        # does not change state anymore


class State_bomb(STATE, State_Nonresponsive):
    _clue = 'x'

    def __init__(self, node):
        """
        does not change state anymore but changes neighb. states once at init
        :param node: a Node instance: the reference to the object, that is in
        the State_bomb
        """
        self._state = 'x'  # setting does not change this
        self.node = node
        r, c = self.node.position  # deprec
        self.node.context.b[r][c] = 'x'  # deprec
        self.node.questionmarks = set()

        # 1)  reduce total no. of bombs by one
        self.node.context.remain_bomb -= 1

        # 2) remove self from neighb. ? & reduce neighb state by 1
        for n in self.node.neighb_inst:
            n._state -= 1
            n.STATE.discardQ(self.node)


class State_Q(STATE):
    _clue = '?'

    def __init__(self, node):
        """

        :param node: a Node instance: the reference to the object, that is in
        the State_Q
        """
        # intialise state
        self.node = node
        self._state = 0

    def discardQ(self, other):
        self.node.questionmarks.discard(other)


class State_Clue(STATE):

    def __init__(self, node, old_state=0):
        """

        :param node: a Node instance: the reference to the object, that is in
        the State_Clue
        :param old_state:
        """
        self.node = node
        # 1) call open:
        value = self.node.context.open(*self.node.position)
        self._clue = value

        if value != 0:
            # add new information (to existing negative clue if any)
            self.clue = value
            self._state = old_state + int(value)

            # 2) remove from neighb's ?
            for n in node.neighb_inst:
                n.STATE.discardQ(self.node)

            # does not change state anymore
            # but changes neighb. states
            self.check_STATE_change()

        else:
            # this allows to start recursion from the zeros
            self._state = 0
            self.node.STATE = State_zero(self.node)

    def discardQ(self, other):
        # TODO whenever a questionmarks is discarded from a clue, the instance
        #  must be checked for its state. - if this is the convention,
        #  state property will no longer be necessary: once in State_Clue, (and it's init is complete)
        #  only bombs affect the state of State_Clue - and bombs always come with
        #  a discard of Q for this Node.
        self.node.questionmarks.discard(other)
        self.check_STATE_change()

    def check_STATE_change(self):
        # all questionmarks can be opened
        if self._state == 0:
            while bool(self.node.questionmarks):
                q = self.node.questionmarks.pop()
                if not isinstance(q, State_Clue):
                    q.STATE = State_Clue(q, q._state)


        # all surrounding '?' are bombs
        elif self._state == len(self.node.questionmarks):
            while bool(self.node.questionmarks):
                bomb = self.node.questionmarks.pop()
                if not isinstance(bomb, State_bomb):
                    bomb.STATE = State_bomb(bomb)

# if __name__ == '__main__':
#     from Minesweeper.StatePattern.Node import Node
#
#
#     class Context:
#         dim = (1, 2)
#         remain_bomb = 2
#
#         def open(self, r, c):
#             if (r, c) == (0, 0):
#                 return 0
#             elif (r, c) == (0, 1):
#                 return 1
#
#
#     n = Node(position=(0, 0), context=Context())  # context required for find_neighb
#     neighb = Node(position=(0, 1), context=Context())
#     neighb.neighbours == set(((0, 0),))
#     n.neighbours == set(((0, 1),))
#     n.neighb_inst = set([neighb, ])
#     n.questionmarks = set([neighb, ])
#     neighb.neighb_inst = set([n, ])
#     neighb.questionmarks = set([n, ])
#
#     n.__repr__()
#     [n.clue, neighb.clue] == [0, 1]
#
#     n.STATE = State_Clue(n, 0)
#     [n.clue, neighb.clue] == [0, 1]
#
#     n.__repr__()
