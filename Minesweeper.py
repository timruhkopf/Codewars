from itertools import product, permutations  # permutations is deprec
import sys

sys.setrecursionlimit(10 ** 6)

DEBUG = True


class Position:
    game = None
    dim = 1, 1

    def __init__(self, position, clue='?'):
        self.position = position
        neighbours, intermediate = self._find_neighbours(position)
        self.neighbours = neighbours
        self.intermediate = intermediate

        self.neighb_inst = set()
        self.intermediate_inst = set()

        self._clue = clue
        self._state = 0

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
        return other in self.neighb_inst

    def isintermediate(self, other):
        return other in self.intermediate_inst

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
        # open all questionmarks by state hitting 0
        if value == 0:
            self._state = 0
            toopen = self.questionmarks.copy()
            for q in toopen:
                Position.game.open(*q.position)

            for n in self.neighb_inst:
                if n.state == len(n.questionmarks):
                    n.found_bomb()

        # default case, setting the received value
        else:
            self._state = value
            if self.state == len(self.questionmarks):
                self.found_bomb()

    def found_bomb(self):
        self._state = 0
        toopen = self.questionmarks.copy()
        for q in toopen:
            q._clue = 'x'

            # Now two loops to ensure the state is correct when proceed
            for n in q.neighb_inst:
                n._state -= 1
                if q in n.questionmarks:
                    n.questionmarks.remove(q)

            for n in q.neighb_inst:
                n.state = n._state

    @staticmethod
    def _find_neighbours(position):
        """returns the set of all neighbours (excluding self's position).
        all of them are bound checked"""
        r, c = position
        cond = lambda r, c: 0 <= r < Position.dim[0] and 0 <= c < Position.dim[1]
        square = lambda kernel: set((r + i, c + j) for i in kernel for j in kernel
                                    if cond(r + i, c + j) and cond(r + i, c + j))

        # find the direct neighbours
        neighb = square(kernel=(-1, 0, 1))

        # finding the bounded intermediate neighbours
        intermediate = square(kernel=(-2, -1, 0, 1, 2))
        intermediate.difference_update(neighb)

        neighb.remove((r, c))
        return neighb, intermediate


class Game:
    def __init__(self, map, result=None):
        """
        Game class allows interactive debugging in Pycharm
        :param map: true map
        """
        self.map = self.parse_map(map)
        self.dim = len(self.map), len(self.map[0])  # no. of rows, columns of map
        Position.dim = self.dim  # preset for all positions

        zeroind = [i for i, val in enumerate(map.replace(' ', '').replace('\n', '')) if val == '0']
        self.zerotup = [(ind // self.dim[1], ind % self.dim[1]) for ind in zeroind]

        if result is not None:
            self.result = self.parse_map(result)
            self.count = result.count('x')  # no. of bombs

        tuples = [(i, j) for i in range(self.dim[0]) for j in range(self.dim[1])]
        self.clues = {k: Position(k) for k in tuples}  # {position_tuple: Position_instance}

        # setting up the neighbourhood structure
        for inst in self.clues.values():
            inst.neighb_inst = set(self.clues[k] for k in inst.neighbours)
            inst.intermediate_inst = set(self.clues[k] for k in inst.intermediate)
            inst.questionmarks = inst.neighb_inst.copy()

        self.exacly_one = list()

    def __repr__(self):
        return self.encode_map_from_Position()

    @staticmethod
    def parse_map(map):
        return [row.split() for row in map.split('\n')]

    def encode_map_from_Position(self):
        gamemap = [['' for i in range(self.dim[1])] for j in range(self.dim[0])]
        for (r, c), inst in self.clues.items():
            gamemap[r][c] = str(inst)

        return '\n'.join(' '.join(row) for row in gamemap)

    def open(self, row, column):

        if self.clues[(row, column)].clue == '?':

            if DEBUG:
                value = int(self.result[row][column])
            else:
                value = open(row, column)

            if value == 'x':
                raise ValueError('What a bummer.')

            inst = self.clues[(row, column)]
            for n in inst.neighb_inst:
                n.questionmarks.remove(inst)

            inst.clue = value

    def superset_solver(self):
        # first find the neighbours to remaining questionmarks
        inquestion = set(n for q in self.clues.values()
                         for n in q.neighb_inst
                         if q.clue == '?' and n.clue != '?')  # TODO remove this simplification

        # Deprec: too many combinations
        # candidates = ([inst1, inst2] for inst1, inst2 in permutations(inquestion, 2)
        #               if (inst1.isneighb(inst2) or inst1.isintermediate(inst2))
        #               and (inst1._state == 1 or inst2._state == 1))  # TODO remove this simplification

        # most informative intersections start with:
        single = set(n for n in inquestion if n._state == 1)
        candidates = ([inst1, inst2] for inst1, inst2 in product(single, inquestion)
                      if (inst1.isneighb(inst2) or inst1.isintermediate(inst2)))

        for inst1, inst2 in candidates:
            a = inst1.questionmarks
            b = inst2.questionmarks

            if b.issuperset(a):  # SUPERSET
                remain = (b - a)

                # remaining can be opened
                if inst2._state - inst1._state == 0:  # since inst1 is subset
                    toopen = remain.copy()
                    for n in toopen:
                        self.open(*n.position)

                # remaining are bombs
                elif len(remain) == len(b):
                    for n in remain:
                        n.found_bomb()

                # merely found an exacly one
                else:
                    intersect = a.intersection(b)
                    if inst1._state==1: # it cannot be a 2 out of 3. but could be 2 hidden in 3 Notice this condition is currently always true (by design)
                        self.exacly_one.append(intersect)


    def solve(self):
        # (0) causal (state) communication logic from initial zeros
        for zero in self.zerotup:
            self.open(*zero)

        print('')

        # (1) exacly one bomb in questionmarks logic
        before = str(self)
        after = before
        while before == after:
            self.superset_solver()
            after = str(self)

        # (2) Endgame logic based on number of bombs.

        # ambiguity?
        if bool([inst._clue for inst in self.clues.values() if inst._clue == '?']):
            return '?'
        else:
            return Position.game


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
    return str(Position.game.solve())

#
# gamemap = """
# ? ? ? ? ? ?
# ? ? ? ? ? ?
# ? ? ? 0 ? ?
# ? ? ? ? ? ?
# ? ? ? ? ? ?
# 0 0 0 ? ? ?
# """.strip()
# result = """
# 1 x 1 1 x 1
# 2 2 2 1 2 2
# 2 x 2 0 1 x
# 2 x 2 1 2 2
# 1 1 1 1 x 1
# 0 0 0 1 1 1
# """.strip()
# game1 = Game(gamemap, result)
# assert solve_mine(gamemap, game1.count, result) == result

gamemap = """
? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? ? ? ? ? ?
? ? ? ? 0 0 ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0 ? ? ? ? ? 0 0 0
""".strip()

result = """
1 2 x 1 0 0 0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 1 1 1 1 x 1
1 x 2 1 0 0 0 0 0 0 0 0 1 1 1 0 0 0 1 1 1 1 x 1 1 1 1
1 2 2 1 0 0 1 1 1 0 0 0 0 0 0 0 0 0 1 x 2 2 1 1 0 0 0
0 1 x 2 1 2 2 x 2 1 0 0 0 0 0 0 0 0 1 3 x 3 1 1 0 0 0
0 1 1 2 x 2 x 3 x 1 0 0 0 0 0 0 0 0 0 2 x 3 x 1 0 0 0
""".strip()
game1 = Game(gamemap, result)
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

# Deterministic board
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

