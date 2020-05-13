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

        # TODO: fix mistake where self.questionmark produces neighb with clue 'x'
        if bool(toopen):
            self.bombastic(bombs=toopen)

    @staticmethod
    def bombastic(bombs):
        for b in bombs:
            if b._clue == '?': # needed until deep copy problem in found_bomb is not solved
                b._clue = 'x'
                b.game.remain_bomb -= 1

                for n in b.neighb_inst:
                    n._state -= 1
                    if b in n.questionmarks:
                         n.questionmarks.discard(b)

                for n in b.neighb_inst:
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

        neighb.discard((r, c))
        return neighb, intermediate


class Game:
    def __init__(self, map, n, result=None):
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

        self.remain_bomb = n
        self.exacly_one = list()

    def __repr__(self):
        return self.encode_map_from_Position()

    @staticmethod
    def parse_map(map):
        return [row.split() for row in map.split('\n')]

    def encode_map_from_Position(self):
        g = [' '.join([str(self.clues[(r, c)])
                       for c in range(self.dim[1])]) for r in range(self.dim[0])]
        return '\n'.join(g)

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
                n.questionmarks.discard(inst)

            inst.clue = value

    def superset_solver(self):
        # first find the neighbours to remaining questionmarks
        inquestion = set(n for q in self.clues.values()
                         for n in q.neighb_inst
                         if q.clue == '?' and n.clue not in ['?', 'x'])  # TODO discard this simplification

        # Deprec: too many combinations
        # candidates = ([inst1, inst2] for inst1, inst2 in permutations(inquestion, 2)
        #               if (inst1.isneighb(inst2) or inst1.isintermediate(inst2))
        #               and (inst1._state == 1 or inst2._state == 1))  # TODO discard this simplification

        # most informative intersections start with:
        single = set(n for n in inquestion if n._state == 1)
        candidates = ([inst1, inst2] for inst1, inst2 in product(single, inquestion)
                      if (inst1.isneighb(inst2) or inst1.isintermediate(inst2)) and inst2._state != 0)

        for inst1, inst2 in candidates:
            a = inst1.questionmarks
            b = inst2.questionmarks
            # print(inst1.position, inst2.position)
            #
            # if (inst1.position, inst2.position) == ((26, 26), (28, 26)):
            #     print()
            if b.issuperset(a) and bool(a):  # SUPERSET and a was not filled
                # in the meantime whilest iterating over candidates
                remain = (b - a)

                # remaining can be opened
                if inst2._state - inst1._state == 0:  # since inst1 is subset
                    toopen = remain.copy()
                    for n in toopen:
                        self.open(*n.position)

                # remaining are bombs
                elif len(remain) == inst2._state - inst1._state:
                    Position.bombastic(bombs=remain)

            elif inst2._state - inst1._state == len(a.union(b) - a):
                remain = a.union(b) - a
                Position.bombastic(bombs=remain)

        # search for all direct neighbor triplet who share the same questionmarks to make inferrence about bomb location
        inquestion = set(n for q in self.clues.values()
                         for n in q.neighb_inst
                         if q.clue == '?' and n.clue not in ['?', 'x'])

        single = set(n for n in inquestion if n._state == 1)
        candidates2 = ([inst1, inst2, inst3] for inst1, inst2, inst3 in product(single, inquestion, single)
                       if (inst1.isneighb(inst2) and inst3.isneighb(inst2)) and inst2._state != 0 and inst1 != inst3)

        for inst1, inst2, inst3 in candidates2:
            a = inst1.questionmarks
            b = inst2.questionmarks
            c = inst3.questionmarks
            union = a.union(c)

            if b.issuperset(union) and bool(a) and bool(b):
                remain = (b - union)

                if inst2._state - inst1._state - inst3._state == 0 \
                        and len(union) == len(a) + len(c):  # otherwise the code opens fields which it cannot
                    toopen = remain.copy()
                    for n in toopen:
                        self.open(*n.position)

                    # remaining are bombs
                elif len(remain) == inst2._state - inst1._state - inst3._state:
                    Position.bombastic(bombs=remain)

    def endgame(self):
        inquestion = set(n for q in self.clues.values()
                         for n in q.neighb_inst
                         if q.clue == '?' and n.clue not in ['?', 'x'])

        single = set(n for n in inquestion if n._state == 1)

        # append all exactly ones coming from state 1 fields
        for _ in single:
            if _.questionmarks not in self.exacly_one:
                self.exacly_one.append(_.questionmarks)

        # append exactly ones coming from higher state fields that are cut by exactly ones and building exactly ones
        # by their own
        for _ in inquestion:
            for i in self.exacly_one:
                if _.questionmarks.issuperset(i) and _._state == 2 \
                        and _.questionmarks.difference(i) not in self.exacly_one:
                    self.exacly_one.append(_.questionmarks.difference(i))

        # remaining questionmarks that are not in exactly._one
        remain_q = [i for i in self.clues.values() if i.clue == '?' and all(i not in _ for _ in self.exacly_one)]


    def solve(self):
        # (0) causal (state) communication logic from initial zeros
        for zero in self.zerotup:
            self.open(*zero)

        print('')

        # (1) exacly one bomb in questionmarks logic
        before = True
        after = False
        while before != after:
            before = str(self)
            self.superset_solver()
            after = str(self)

        # (2) Endgame logic based on number of bombs.
        if bool(self.remain_bomb):
            self.endgame()

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
    if n == 0: return '0'
    Position.game = Game(gamemap, n, resultmap)
    return str(Position.game.solve())

# !!!!!!!!! ENDGAME ENDGAME ENDGAME !!!!!!
gamemap = """
0 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? ? ?
0 ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ? 0
? ? ? ? 0 0 0 0 0 0
? ? ? 0 0 0 0 0 0 0
""".strip()
result = """
0 0 0 0 1 1 1 1 1 1
0 0 0 1 2 x 2 2 x 1
0 1 1 2 x 2 2 x 2 1
1 2 x 2 1 1 1 1 1 0
1 x 2 1 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
""".strip()
game1 = Game(gamemap, 6,  result)
assert solve_mine(gamemap, game1.count, result) == result
#
gamemap = """
? ? ? 0 0 ? ? ? ? ? ? 0 0 ? ? ? ?
? ? ? 0 0 ? ? ? ? ? ? 0 0 ? ? ? ?
0 0 0 0 0 ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ?
0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
? ? ? 0 0 0 0 0 0 0 0 0 0 ? ? ? ?
? ? ? 0 0 0 0 0 0 0 0 0 0 ? ? ? ?
""".strip()
result = """
1 x 1 0 0 2 x 2 1 x 1 0 0 1 x x 1
1 1 1 0 0 2 x 3 2 1 1 0 0 1 3 4 3
0 0 0 0 0 1 2 x 1 0 0 0 0 0 1 x x
0 0 0 0 0 0 1 1 1 0 0 0 0 0 1 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
1 1 1 0 0 0 0 0 0 0 0 0 0 1 2 x 1
1 x 1 0 0 0 0 0 0 0 0 0 0 1 x 2 1
""".strip()
game1 = Game(gamemap, 12, result)
assert solve_mine(gamemap, game1.count, result) == result

gamemap = """
0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ? 0 0 0
0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? 0 0 ? ?
0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0 0 ? ?
0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
0 ? ? ? 0 ? ? ? 0 0 0 0 0 ? ? ? 0 ? ? ?
0 ? ? ? 0 ? ? ? ? ? ? 0 0 ? ? ? ? ? 0 0
0 ? ? ? 0 ? ? ? ? ? ? 0 0 ? ? ? ? ? 0 0
0 ? ? ? 0 0 0 ? ? ? ? 0 0 0 0 ? ? ? 0 0
0 ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0
0 ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 ? ? ? ? 0
0 ? ? ? 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? 0
? ? ? ? 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? 0
? ? 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? ?
? ? ? ? 0 0 ? ? ? ? ? 0 ? ? ? 0 0 ? ? ?
? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ? 0 0 0 0
0 ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
0 0 0 0 ? ? ? 0 0 0 0 0 ? ? ? ? 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? 0 ? ? ? ? 0 0 0 0
? ? ? ? ? 0 0 ? ? ? ? ? ? ? ? ? ? ? ? 0
? ? ? ? ? 0 0 ? ? ? ? ? ? 0 ? ? ? ? ? ?
? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ?
? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 ? ? ?
? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 ? ? ?
? ? ? ? ? ? 0 0 0 0 0 0 0 0 0 0 0 ? ? ?
""".strip()
result = """
0 1 1 2 1 1 0 0 0 1 1 2 2 2 2 x 1 0 0 0
0 1 x 2 x 1 0 0 0 1 x 3 x x 3 2 1 0 0 0
0 1 1 2 1 1 0 0 0 1 2 x 3 3 x 1 0 0 1 1
0 0 0 1 1 1 0 0 0 0 1 1 1 1 1 1 0 0 1 x
0 0 0 1 x 1 0 0 0 0 0 0 0 0 0 0 0 1 2 2
0 1 1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 x 1
0 1 x 1 0 1 1 1 0 0 0 0 0 1 1 1 0 1 1 1
0 1 1 1 0 1 x 2 2 2 1 0 0 1 x 2 1 1 0 0
0 1 1 1 0 1 1 2 x x 1 0 0 1 1 2 x 1 0 0
0 1 x 1 0 0 0 1 2 2 1 0 0 0 0 2 2 2 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
0 1 1 1 0 0 0 0 0 1 1 1 0 0 0 1 2 x 1 0
0 1 x 1 0 0 0 0 0 1 x 2 1 1 0 1 3 3 2 0
1 2 1 1 0 0 0 0 0 1 1 2 x 1 0 2 x x 1 0
x 1 0 0 0 0 0 0 0 0 0 1 1 1 0 2 x 4 3 2
1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 2 x x
1 2 x 1 0 0 1 2 3 2 1 0 1 1 1 0 0 1 2 2
1 x 3 3 1 1 1 x x x 1 0 2 x 2 0 0 0 0 0
1 2 x 2 x 1 2 3 4 2 1 0 2 x 3 1 0 0 0 0
0 1 1 2 2 2 2 x 1 0 0 0 1 2 x 1 0 0 0 0
0 0 0 0 1 x 2 1 1 0 0 0 1 2 2 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0 1 x 2 1 0 0 0 0
0 0 0 0 0 0 0 1 2 2 1 0 1 2 x 1 0 0 0 0
1 1 1 1 1 0 0 1 x x 2 1 1 1 2 2 2 1 1 0
x 2 3 x 2 0 0 1 2 2 2 x 1 0 1 x 2 x 2 1
2 x 3 x 2 0 0 0 0 0 1 2 2 1 1 1 2 1 2 x
2 3 3 3 2 1 0 0 0 0 0 1 x 1 0 0 0 1 2 2
x 2 x 2 x 1 0 0 0 0 0 1 1 1 0 0 0 1 x 1
1 2 1 2 1 1 0 0 0 0 0 0 0 0 0 0 0 1 1 1
""".strip()
game1 = Game(gamemap, 58, result)
assert solve_mine(gamemap, game1.count, result) == result
# #

gamemap = """
0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? ? ? ? ? ?
? ? 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? 0 ? ? ? ? ? ?
? ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? 0 ? ? ? ? ? ?
0 ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0
""".strip()

result = """
0 0 0 1 x 1 1 x 1 0 0 0 0 0 1 1 1 0 0 1 x 3 x 3 1 2 1
1 1 0 1 1 1 1 1 1 0 0 0 0 0 1 x 1 1 1 2 1 3 x 3 x 2 x
x 2 1 1 0 0 0 0 0 0 1 1 1 0 1 1 1 1 x 1 0 2 2 3 1 3 2
1 2 x 1 0 0 0 0 0 0 1 x 1 0 0 0 0 1 1 1 0 1 x 2 1 2 x
0 1 1 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 1 2 3 x 2 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 x 2 1 0
""".strip()
game1 = Game(gamemap, result)
assert solve_mine(gamemap, game1.count, result) == '?'

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
