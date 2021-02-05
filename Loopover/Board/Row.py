from collections import deque


class Node:
    current = dict()
    target = dict()  # target coordinates value: (row, col)

    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __repr__(self):
        return str(self.value)


class Context:
    # Default only for test cases, to initalise Row with no context
    solution = []


class Row(list):
    direct = ('L', 'R')
    context = Context()

    def __init__(self, iterable, ind, context=None):
        """
        :param iterable: an ordered collection of Node instances
        :param ind: row index
        :param context: obj; reference to an obj with attribute obj.solution.
        """
        super(Row, self).__init__(iterable)
        self.queue = deque(maxlen=len(iterable))
        self.ind = str(ind)

        if context is not None:
            self.context = context

    def shift(self, direction):
        """
        :param direction: integer. value of integer indicates the number of
        repeated shifts. the sign indicates a left(-) or right(+) shift,
        :return None, but extends the the context object's solution by the appropriate shift(s)
        (e.g. direction = -2, ind=0 ['L0, 'L0'])
        """
        # overwrites at each step the queue, since a shift in orthogonal direction
        # does not change queue
        self.queue.extend([node.value for node in self])
        self.queue.rotate(direction)
        for node, v in zip(self, self.queue):
            node.value = v
            Node.current[v] = node.position  # still efficient as merely pointer
            # to immutable tuple is shared (no new tuple is created)

        # parse the direction literal(s) and append to solution
        self.context.solution.extend([self.direct[direction > 0] + self.ind] * abs(direction))

    def shortest_shiftLR(self, j, c):
        """
        :param j: current position in Row
        :param c: target position in Row
        :returns minimal shifting length given this rows length: negative values
        indicate a "left", positive indicate "right" shift.
        """
        # [leftdistance, rightdistance]
        return min([-((len(self) - (c - j)) % len(self)), (len(self) + c - j) % len(self)], key=abs)

    def toList(self):
        """:return the list of the nodes' values rather then the list of nodes"""
        return [node.value for node in self]


class Column(Row):
    direct = ('D', 'U')
    context = Context()

    def __init__(self, iterable, ind, context=None):
        """
        :param iterable: ordered collection of Node instances. ordering is bottom to top,
        such that D shift corresponds to L in Row (and U to R)
        :param ind: column index
        :param context"""
        Row.__init__(self, iterable, ind, context)
