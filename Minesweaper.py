class Game:
    def __init__(self, map, result):
        """Game class allows interactive debugging in Pycharm
        :param map: true map"""
        self.map = self.parse_map(map)
        self.result = self.parse_map(result)
        self.count = 0  # Fixme: number of x in final map

    def __repr__(self):
        return self.map # Fixme: string must be interleaved with spaces & \n

    def parse_map(self, map):
        """:return nested list of strings"""

        # NOTICE:
        # """
        # ...     1 x 1 1 x 1
        # ...     2 2 2 1 2 2
        # ...     2 x 2 0 1 x
        # ...     2 x 2 1 2 2
        # ...     1 1 1 1 x 1
        # ...     0 0 0 1 1 1
        # ...     """ ==
        #  '\n    1 x 1 1 x 1\n    2 2 2 1 2 2\n    2 x 2 0 1 x\n    2 x 2 1 2 2\n    1 1 1 1 x 1\n    0 0 0 1 1 1\n    '

        pass

    def open(self, row, column):
        value = self.result[row][column]
        if value == 'x':
            raise ValueError('What a bummer.')

        # CAREFULL: make sure, the challenge actually allows us to maintain state this way
        self.map[row][column] = value
        return value



class Position:

    def __init__(self):
        self.neighbours = None
        self.clue = None
        self.bombds = None  # known adjacent bomb positions. len of bombs == clue?
        # --> uncover all remaining neighbours.

        self.exacly_one = None  # a list of positions, at which it is known to
        # have exacly (one or two) bombs - such that this info may uncover all others

    def broadcast_bomb(self):
        # (remove the found bomb from self.neighbours)
        # tell relevant neighbours about the bomb (i.e. the bombs neighbours)
        pass

    def die(self):
        # remove this position instance from classattribute once all bombs
        # are found & neighbours are uncovered
        pass


    game = Game(map)
    open = game.open


def solve_mine(map, n):
    """
    https://www.codewars.com/kata/57ff9d3b8f7dda23130015fa

    :param map: string map, containing the 'board' with all zeros uncovered &
    ? as unknown values.
    :param n: number of mines on that board.
    :return: a solved string map, containing only integers & 'x'`s for bomb markers

    """

    # uncovering mines using a method "open(row,column)"
    # Game.open(row, column) ????
    #  It will return a number that is how many mines around this grid.
    #  If there is an error in your logical reasoning, when you use the open
    #  method to open a grid, but there is a mine hidden in this grid, then
    #  the test will fail. Please note, method open only return a number,
    #  but did not modify the map, you should modify the map by yourself.

    # call open
    pos = (1,2)
    #val = open(*)

    # If the game can not got a valid result, should return "?"

    pass


if __name__ == '__main__':
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
