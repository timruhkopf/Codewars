# class Stone:
#     def __init__(self, coord, color='b'):
#         self.color = color
#         self.icon = {'w': 'o', 'b': 'x'}[color]
#
#         self.coord = coord
#
#         x, y = coord
#         self.neighb = [(x - i, y - j) for i in [-1, 1] for j in [-1, 1]]
#
#     # Consider (1) moving these methods to Go --OR-- (2) make stones instance aware
#     def check_liberties(self):
#         self.liberties = None
#         pass
#
#     def update_neigb(self, other):
#         pass


# consider using this to keep track of groups liberties (maybe even without stone instances)
class Group:
    # FIXME: how to access the board? inheritance?
    def __init__(self, firststone, color):
        self.member = [firststone]
        self.liberties = set()  # set of positions
        pass

    def update_liberties(self):
        pass

    def merge(self, other):
        self.liberties = None  # += other.liberties?
        self.member.extend(other.member)
        pass

    def die(self):
        pass


class Go:
    _groups = dict()  # groupID: Group

    def __init__(self, height, width=None):
        """https://www.codewars.com/kata/59de9f8ff703c4891900005c"""
        if width is None:
            width = height

        if height > 25 or width > 25:
            raise ValueError('max board size in any dimension is 25')
        # required attribute
        self.size = {'height': height, 'width': width}

        # TODO: make board property: getter method uses dict representation
        self.board = [['.' for i in range(width)] for j in range(height)]

        # for ease of fetching neighbours
        self.affiliation = dict()  # {position: groupID}  # dict to keep track of all group members
        # i.e. asking neighbours' groupID here

        self.history = []  # strings of positions e.g. "A7" allows to check invalid
        # KO placements -i.e. player places stone at his turn in the same position
        # he did on his previous turn.
        # self.move_counter = 0 # == len(self.history)

    def handicap_stones(self, stones):
        stone_pos = {9: ['G7', 'C3', 'G3', 'C7', 'E5'],
                     13: ['10I', '4C', '4I', '10C', '7F', '6C', '7I', '3F', '9F'],
                     19: ['16O', '4C', '16C', '4O', '10I', '10C', '10O', '16I', '4I']}

        if list(self.size.values()) != [19, 19] and list(self.size.values()) != [13, 13] and list(size.values()) != [9, 9]:
            raise ValueError('boardsize is not suitable for handicap stones')
        elif len(stone_pos[self.size['height']]) < stones:
            raise ValueError('too many handicap stones for given boardsize')
        elif any(j == 'x' for i in board for j in i):
            # do this by _groups
            raise ValueError('game has already started or you called handicap_stones twice')
        else:
            ls = stone_pos[self.size['height']][0:stones]
            move(ls)

            # for i, j in stone_pos[self.size['height']][0:stones]:
            #     self.board[i][j] = 'x'


    def move(self, positions):
        """positions may take multiple values:
        move("4A", "5A", "6A")"""
        for position in positions:
            r, c = position

            if self._valid_move(position):
                self.board[r][c] = ['x', 'o'][len(self.history) % 2]
                self.history.append(position)

            # Consider: check neighbours of position and add stone to a group if
            # there exists a stone of same color on cross. BE AWARE of "linking stones"
            cond = lambda r, c: r >= 0 and r < self.size['height'] and c >= 0 and c < self.size['width']
            neighb = [(r + i, c + j) for i in [-1, 0,  1] for j in [-1, 1] if cond(r + i, c + j)]

            # update affiliation

            # update groups
            # (1) membership
            # (2) liberties union. (same color) (to avoid circular patterns and false counting)
            # different color: difference

        pass

    def parse_position(self, move):
        hor = [chr(i) for i in range(ord('A'), ord('Y') + 1)][0:self.size['width']]
        ver = [i for i in reversed(range(self.size['height'] + 1))]

        if int(move[0:-1]) not in ver or move[-1] not in hor:
            raise ValueError('You are out of bounds')
        else:
            return ver[int(move[0])], hor.index(move[1])

    def _valid_move(self, position):
        # ToDO check
        #  (1) if stone already @ pos.
        r, c = position
        if self.board[r][c] != '.':
            raise ValueError('cannot place a stone on top of another stone')

        # ToDO check
        #  (2) if KO (look at history)
        #  (3) suicide move (before assigning: check that same colored groups dont die)
        #   what about connecting stones?
        #  (4) check boundary
        pass

    def turn(self):  # FIXME: property getter not class method
        # getter of current Turn color:
        return ['black', 'white'][len(self.history) % 2]

    def pass_turn(self):
        # not making a move, incrementing the move_counter (==>)
        # Consider adding an empty string to self.history. makeing history &
        # KO consistent
        pass

    def get_position(self, position):
        """
        :param position: TODO check valid!
        :return: 'x', 'o' or '.'
        """

        position = self.parse_position(position)
        i, j = position

        if self.board[i][j] != '.':
            return self.affiliation[position].color
        else:
            return '.'

    def rollback(self, steps):
        '''rollback the last game moves'''
        pass

    def reset(self):  # FIXME: CHECK ME!!!
        # remove all attributes of self
        for name in [k for k in self.__dict__.keys() if k != 'size']:
            delattr(self, name)

        # reset groups
        Go._groups = dict()

        # reinstate attributes.
        self.__init__(**self.size)


if __name__ == '__main__':

    go = Go(9)

    from random import choice, randint
    from Test_Codewars import test

    test.describe("Creating go boards")
    test.it("9x9")
    game = Go(9)
    board = [[".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."]]
    test.assert_equals(game.board, board, "Should generate a 9 by 9 board.")
    # close_it()

    test.it("13x13")
    game = Go(13)
    board = [[".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]]
    test.assert_equals(game.board, board, "Should generate a 13 by 13 board.")
    # close_it()

    test.it("19x19")
    game = Go(19)
    board = [[".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]]
    test.assert_equals(game.board, board, "Should generate a 19 by 19 board.")
    # close_it()

    test.it("32x32")
    test.expect_error("Should throw an error. Board cannot be larger than 25 by 25", lambda: Go(32))
    # close_it()
    # close_describe()

    test.describe("Placing stones")
    test.it("Place a black stone")
    game = Go(9)
    game.move("3D")
    test.assert_equals(game.get_position("3D"), "x")
    # close_it()

    test.it("Place a white stone")
    game.move("4D")
    test.assert_equals(game.get_position("4D"), "o")
    # close_it()

    test.it("Can take multiple moves at a time")
    game.move("4A", "5A", "6A")
    test.assert_equals(game.get_position("4A"), "x")
    test.assert_equals(game.get_position("5A"), "o")
    test.assert_equals(game.get_position("6A"), "x")
    # close_it()

    test.it("Cannot place a stone on an existing stone. Raises an error.")
    test.expect_error("3D should be an invalid move", lambda: game.move("3D"))
    test.expect_error("4D should be an invalid move", lambda: game.move("4D"))
    # close_it()

    test.it("Cannot place a stone with out of bounds coordinates. Raises an error.")
    test.expect_error("3Z should be an invalid move", lambda: game.move('3Z'))
    test.expect_error("66 should be an invalid move", lambda: game.move('66'))
    # close_it()
    # close_describe()

    test.describe("Capturing")
    test.it("Black captures single white stone")
    game = Go(9)
    moves = ["4D", "3D", "4H", "5D", "3H", "4C", "5B", "4E"]
    game.move(*moves)
    test.assert_equals(game.get_position('4D'), ".")
    # close_it()

    test.it("Black captures multiple white stones")
    game = Go(9)
    moves = ["6D", "7E", "6E", "6F", "4D", "5E", "5D", "7D",
             "5C", "6C", "7H", "3D", "4E", "4F", "3E", "2E",
             "3F", "3G", "2F", "1F", "2G", "2H", "1G", "1H",
             "4C", "3C", "6H", "4B", "5H", "5B"]
    captured = ["6D", "6E", "4D", "5D", "5C", "4E", "3E", "3F", "2F", "2G", "1G", "4C"]
    game.move(*moves)
    for capture in captured:
        test.assert_equals(game.get_position(capture), ".")
    # close_it()

    test.it("Corner capture")
    game = Go(9)
    moves = ["9A", "8A", "8B", "9B"]
    game.move(*moves)
    test.assert_equals(game.get_position('9A'), ".")
    # close_it()

    test.it("Multiple captures")
    game = Go(9)
    moves = ["5D", "5E", "4E", "6E", "7D", "4F", "7E", "3E", "5F", "4D",
             "6F", "6D", "6C", "7F", "4E", "5E"]
    captured = ["4E", "6D", "6E"]
    game.move(*moves)
    for capture in captured:
        test.assert_equals(game.get_position(capture), ".")
    # close_it()

    test.it("Snapback")
    game = Go(5)
    moves = ["5A", "1E", "5B", "2D", "5C", "2C", "3A",
             "1C", "2A", "3D", "2B", "3E", "4D", "4B",
             "4E", "4A", "3C", "3B", "1A", "4C", "3C"]
    captured = ["4A", "4B", "4C", "3B"]
    game.move(*moves)
    for capture in captured:
        test.assert_equals(game.get_position(capture), ".")
    # close_it()

    test.it("Self-capturing throws an error.")
    game = Go(9)
    moves = ["4H", "8A", "8B", "9B", "9A"]
    test.expect_error("self capturing moves are illegal", lambda: game.move(*moves))
    test.assert_equals(game.get_position("9A"), ".", "Illegal stone should be removed")
    game.move("3B")
    test.assert_equals(game.get_position("3B"), "x", "Black should have another try")
    # close_it()
    # close_describe()

    test.describe("KO Rule")
    test.it("Illegal KO by white")
    game = Go(5)
    moves = ["5C", "5B", "4D", "4A", "3C", "3B",
             "2D", "2C", "4B", "4C", "4B"]
    test.expect_error("Illegal KO move. Should throw an error.", lambda: game.move(*moves))
    game.move("2B")
    test.assert_equals(game.get_position("2B"), "x", "Black should be given another try to place their stone.")
    test.assert_equals(game.get_position("4B"), ".", "Should rollback game before illegal move was made.")
    # close_it()
    # close_describe()

    test.describe("Handicap stones")
    test.it("Three handicap stones on 9x9")
    game = Go(9)
    finalBoard = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', 'x', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', 'x', '.', '.', '.', 'x', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                  ['.', '.', '.', '.', '.', '.', '.', '.', '.']]

    game.handicap_stones(3)
    test.assert_equals(game.board, finalBoard)
    # close_it()
    # close_describe()

    test.describe("Misc")
    test.it("Can get board size")
    game = Go(9, 16)
    test.assert_equals(game.size, {"height": 9, "width": 16})
    # close_it()

    test.it("Can get color of current turn")
    game = Go(9)
    game.move("3B")
    test.assert_equals(game.turn, "white")
    game.move("4B")
    test.assert_equals(game.turn, "black")
    # close_it()

    test.it("Can rollback a set number of turns")
    game = Go(9)
    board = [[".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."]]
    game.move("3B", "2B", "1B")
    game.rollback(3)
    test.assert_equals(game.board, board)
    test.assert_equals(game.turn, "black")
    # close_it()

    test.it("Can pass turn")
    game = Go(9)
    game.pass_turn()
    test.assert_equals(game.turn, "white")
    # close_it()

    test.it("Can reset the board")
    game = Go(9)
    board = [[".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."],
             [".", ".", ".", ".", ".", ".", ".", ".", "."]]

    game.move("3B", "2B", "1B")
    game.reset()
    test.assert_equals(game.board, board)
    test.assert_equals(game.turn, "black")
