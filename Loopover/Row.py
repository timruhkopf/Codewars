from collections import deque


class Node:
    current = dict()
    target = dict()  # target coordinates value: (row, col)

    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __repr__(self):
        return str(self.value)


class Row(list):
    Solution = list()  # allows both row and column instances to comunicate
    #  but is a sensitive area in parallel computing!
    direct = {True: ('L', 'R'), False: ('U', 'D')}  # fixme potentially U D are in wrong order!

    def __init__(self, iterable, ind, row=True):
        """:param iterable: an ordered collection of Node instances
        :param ind: row index of this row
        :param row: boolean: if i am row or column"""
        super(Row, self).__init__(iterable)
        self.queue = deque(maxlen=len(iterable))

        # Identifyer of row object!
        self.row = row  # am i a row?
        self.ind = str(ind)  # row / column index

    def shift(self, direction):
        """:param direction: integer. value of integer indicates the number of
        repeated shifts. the sign indicates a left(-) or right(+) shift"""
        # overwrites at each step the queue, since a shift in orthogonal direction
        # does not change queue

        self.queue.extend([node.value for node in self])
        self.queue.rotate(direction)
        for node, v in zip(self, self.queue):
            node.value = v
            Node.current[v] = node.position  # still efficient as merely pointer
            # to immutable tuple is shared (no new tuple is created)

        self.Solution.extend(self.direction_parser(direction))

    def direction_parser(self, direction):
        """:param direction: integer: number of shifts, left shift is negative, right positive"""
        return [self.direct[self.row][direction > 0] + self.ind] * abs(direction)

    def shortest_shiftLR(self, j, c):
        """
        :param j: current position in Row
        :param c: target position in Row
        :param rowdim: len(Row)
        :returns minimal shifting length given this rows length: negative values
        indicate a "left", positive indicate "right" shift.
        """
        # [leftdistance, rightdistance]
        return min([-((len(self) -(c-j)) % len(self)),  (len(self) + c-j) % len(self)], key=abs)

    def toList(self):
        """:return the list of the nodes' values rather then the list of nodes """
        return [node.value for node in self]

if __name__ == '__main__':
   pass