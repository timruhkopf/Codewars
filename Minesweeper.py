class Position:
    game = None
    dim = 1, 1

    def __init__(self, position, clue='?'):
        self.position = position
        self.neighbours = self._find_neighbours(position)

        self.neighb_inst = set()

        self._clue = clue
        self._state = 0

    def __repr__(self):  # for debugging only
        # return str(self._clue)
        return str((self.position, 'clue:', self._clue, 'state:', self.state))

    def __str__(self):
        return str(self._clue)

    def __hash__(self):  # to support in
        return hash(self.position)

    def __eq__(self, other):  # to support in
        return self.position == other.position

    @property
    def clue(self):
        return self._clue

    @clue.setter
    def clue(self, value):
        # called at open of this position.
        self._clue = value
        self.state = value + self.state


    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        # once the state = 0 is "called" !
        questions = self._find_questionmarks()

        # open all questionmarks by state hitting 0
        if value == 0:
            self._state = 0
            for q in questions:
                Position.game.open(*q.position)

        # found bomb by remaining ?
        elif value == len(questions):
            self._state = 0
            for q in questions:

                if q == self.game.clues[(2, 5)]:
                    print()

                q._clue = 'x'
                for n in q.neighb_inst:
                    n._state -= 1

                for n in q.neighb_inst:
                    if n.state == 0:
                        n.state = 0

        # default case
        else:
            self._state = value

            for neighb in self.neighb_inst - questions:
                if neighb.state != 0:
                    qs = neighb._find_questionmarks()
                    if neighb.state == len(qs):  # check of those neighbours if they are solved
                        neighb._state = 0
                        for q in qs:
                            q._clue = 'x'

                            if q == self.game.clues[(2, 5)]:
                                print()

                            for n in q.neighb_inst:
                                n._state -= 1

                        for q in qs:
                            for n in q.neighb_inst:
                                if n.state == 0:
                                    n.state = 0

    @staticmethod
    def _find_neighbours(position):
        """returns the set of all neighbours (excluding self's position).
        all of them are bound checked"""
        r, c = position
        cond = lambda r, c: 0 <= r < Position.dim[0] and 0 <= c < Position.dim[1]
        neighb = set((r + i, c + j)
                     for i in (-1, 0, 1)
                     for j in (-1, 0, 1)
                     if cond(r + i, c + j) and cond(r + i, c + j))
        neighb.remove((r, c))
        return neighb

    def _find_questionmarks(self):
        """ask neighbours if they are questionmarks"""
        return set(n for n in self.neighb_inst if n.clue == '?')


class Game:
    def __init__(self, map, result=None):
        """
        Game class allows interactive debugging in Pycharm
        :param map: true map
        """
        self.map = self.parse_map(map)
        self.dim = len(self.map), len(self.map[0])  # no. of rows, columns of map
        Position.dim = self.dim  # preset for all positions

        zeroind = [i for i, val in enumerate(gamemap.replace(' ', '').replace('\n', '')) if val == '0']
        self.zerotup = [(ind // self.dim[0], ind % self.dim[0]) for ind in zeroind]

        if result is not None:
            self.result = self.parse_map(result)
            self.count = result.count('x')  # no. of bombs

        tuples = [(i, j) for i in range(self.dim[0]) for j in range(self.dim[1])]
        self.clues = {k: Position(k) for k in tuples}  # {position_tuple: Position_instance}

        # setting up the neighbourhood structure
        for inst in self.clues.values():
            inst.neighb_inst = set(self.clues[k] for k in inst.neighbours)

    def __repr__(self):
        return self.encode_map_from_Position()

    @staticmethod
    def parse_map(map):
        return [row.split() for row in map.split('\n')]

    def encode_map_from_Position(self):
        # EXPERIMENTAL REPRESENTATION METHOD
        gamemap = [['' for i in range(self.dim[0])] for j in range(self.dim[1])]
        for (r, c), inst in self.clues.items():
            gamemap[r][c] = str(inst)

        return '\n'.join(' '.join(row) for row in gamemap)

    def open(self, row, column):
        if self.clues[(row, column)].clue == '?':

            value = int(self.result[row][column])  # FIXME: this is an int not a string!!!
            if value == 'x':
                raise ValueError('What a bummer.')

            inst = self.clues[(row, column)]
            inst.clue = value

    def solve(self):
        """internal solver"""
        for zero in self.zerotup:
            self.open(*zero)


def solve_mine(gamemap, n, resultmap=None):
    """
    surrogate solver to match this katas desired interface
    https://www.codewars.com/kata/57ff9d3b8f7dda23130015fa

    :param map: string map, containing the 'board' with all zeros uncovered &
    ? as unknown values.
    :param n: number of mines on that board.
    :return: a solved string map, containing only integers & 'x'`s for bomb markers

    """
    Position.game = Game(gamemap, resultmap)
    Position.game.solve()


gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()
result = """
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip()
game1 = Game(gamemap, result)
# game.open_result = open_result(result)
# print(game.open_result(5, 1))  # FIXME: temporary workaround
assert solve_mine(gamemap, game1.count, result) == result

# Ambivalent state
gamemap = """
0 ? ?
0 ? ?
""".strip()
result = """
0 1 x
0 1 1
""".strip()
game = Game(gamemap, result)
# game.open_result = open_result(result)
assert solve_mine(gamemap, game.count, result) == "?"

gamemap = """
? ? ? ? 0 0 0
? ? ? ? 0 ? ?
? ? ? 0 0 ? ?
? ? ? 0 0 ? ?
0 ? ? ? 0 0 0
0 ? ? ? 0 0 0
0 ? ? ? 0 ? ?
0 0 0 0 0 ? ?
0 0 0 0 0 ? ?
""".strip()
result = """
1 x x 1 0 0 0
2 3 3 1 0 1 1
1 x 1 0 0 1 x
1 1 1 0 0 1 1
0 1 1 1 0 0 0
0 1 x 1 0 0 0
0 1 1 1 0 1 1
0 0 0 0 0 1 x
0 0 0 0 0 1 1
""".strip()
game = Game(gamemap, result)
# game.open_result = open_result(result)
assert solve_mine(gamemap, game.count, result) == result

# Huge ambivalent state
gamemap = """
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
""".strip()
result = """
1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
""".strip()
game = Game(gamemap, result)
# game.open_result = open_result(result)
assert solve_mine(gamemap, game.count, result) == "?"

# differently shaped ambivalent state
gamemap = """
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? 0 ? ? ?
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? ? ? ? 0
? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ?
? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ?
? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ?
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
""".strip()
result = """
0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
""".strip()
game = Game(gamemap, result)
# game.open_result = open_result(result)
assert solve_mine(gamemap, game.count, result) == "?"
