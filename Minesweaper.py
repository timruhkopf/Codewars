class Game:
    def __init__(self, map, result=None):
        """
        Game class allows interactive debugging in Pycharm
        :param map: true map
        """
        self.map = self.parse_map(map)
        if result is not None:
            self.result = self.parse_map(result)
            self.count = result.count('x')  # number of bombs

    def __repr__(self):
        return self.encode_map(self.map)

    @staticmethod
    def parse_map(map):
        """:return nested list of strings"""
        return [row.split() for row in map.split('\n')]

    @staticmethod
    def encode_map(map):
        """method to get the desired format of the challenge (pass in solved)"""
        return '\n'.join(' '.join(row) for row in map)

    def open(self, row, column):
        value = self.result[row][column]
        if value == 'x':
            raise ValueError('What a bummer.')

        # CAREFULL: make sure, the challenge actually allows us to maintain state this way
        self.map[row][column] = value
        return value


class Position:
    clues = dict()  # {position_tuple: Position_instance} # CONSIDER moving this to class Game!
    rub, cub = 1, 1  # row/colum upper dim of map overwritten @ each solve_mine call!

    def __init__(self, position, clue):
        self.position = position
        self.neighbours = None
        self.clue = clue
        self.adja_bombds = list()  # known adjacent bomb positions. len of bombs == clue?
        # --> uncover all remaining neighbours.

        self.exacly_one = None  # a (nested) list of positions, at which it is known to
        # have exacly (one or two) bombs - such that this info may uncover all others

    def broadcast_bomb(self, bomb_position):
        """remove the found bomb from self.neighbours &
        tell relevant neighbours about the bomb (i.e. the bombs neighbours)
        & todo if self.exacly_one is maintained, update self.exacly_one & others!"""

        bomb_neighb = self._find_neighbours(bomb_position)  # Experimental: when
        # each field of the board has its own position instance,
        # this becomes a lookup: Position.clues[bomb_position].neighbours

        for neighb in bomb_neighb:
            Position.clues[neighb].bomb.extend(bomb_position)

    @staticmethod
    def _find_neighbours(position):
        """returns the list of all neighbours (excluding self's position).
        all of them are bound checked"""
        r, c = position
        cond = lambda r, c: 0 <= r <= Position.rub and 0 <= c <= Position.cub
        neighb = [(r + i, c + j)
                  for i in (-1, 0, 1)
                  for j in (-1, 0, 1)
                  if cond(r + i, c + j) and cond(r + i, c + j)]
        neighb.remove((r, c))
        return neighb

    def die(self):
        """remove this position instance from classattribute clues once all bombs
        are found & neighbours are uncovered & informed"""
        Position.clues.pop(k=self.position)
        pass


def solve_mine(gamemap, n):
    """
    https://www.codewars.com/kata/57ff9d3b8f7dda23130015fa

    :param map: string map, containing the 'board' with all zeros uncovered &
    ? as unknown values.
    :param n: number of mines on that board.
    :return: a solved string map, containing only integers & 'x'`s for bomb markers

    """
    # FIXME!
    # resetting clues between function calls
    Position.clues = dict()
    game = Game(gamemap)

    # (0) initially open all postions neighbouring zeros
    # CONSIDER moving this to class Game
    zeroind = [i for i, val in enumerate(gamemap.replace(' ', '').replace('\n', '')) if val == '0']
    rowlen = len(gamemap[0])
    zerotup = [(ind % rowlen, ind // rowlen) for ind in zeroind]

    for zero in zerotup:
        for neighb in Position._find_neighbours(zero):
            clue = game.open(*neighb)
            Position.clues.update({neighb: Position(neighb, clue)})


    # (1) parse position
    gamemap = Game.parse_map(gamemap)

    # to ease Position._find_neighbours() calls
    Position.rub = len(gamemap[0])
    Position.cub = len(gamemap)

    # uncovering mines using a method "open(row,column)"
    # Game.open(row, column) ????
    #  It will return a number that is how many mines around this grid.
    #  If there is an error in your logical reasoning, when you use the open
    #  method to open a grid, but there is a mine hidden in this grid, then
    #  the test will fail. Please note, method open only return a number,
    #  but did not modify the map, you should modify the map by yourself.

    # call open
    pos = (1, 2)
    # val = open(*)

    # If the game can not got a valid result, should return "?"

    return Game.encode_map(gamemap)


# CAREFULL: if __name__ == '__main__':
# indentation & muliline string destroy format!
# definite & solvable
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
game = Game(gamemap, result)
assert solve_mine(gamemap, game.count) == result

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
assert solve_mine(gamemap, game.count) == "?"

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
assert solve_mine(gamemap, game.count) == result

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
assert solve_mine(gamemap, game.count) == "?"

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
assert solve_mine(gamemap, game.count) == "?"
