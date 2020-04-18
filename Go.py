from itertools import chain


class Group:
    def __init__(self, firststone, groupID, liberties,  color):
        self.member = [firststone]
        self.groupID = groupID
        self.liberties = set(liberties)  # set of positions
        self.color = color

    def merge(self, *others):
        """:param others: iterable of Group instances"""
        self.liberties.update(
            *(lib for lib in (group.liberties for group in others)))
        self.member.extend((item for group in others for item in group.member))

    def __hash__(self):  # for set behaviour on values
        return self.groupID

class Go:
    def __init__(self, height, width=None):
        """https://www.codewars.com/kata/59de9f8ff703c4891900005c"""
        if width is None:
            width = height

        if height > 25 or width > 25:
            raise ValueError('max board size in any dimension is 25')

        self.size = {'height': height, 'width': width}
        self.board = [['.' for i in range(width)] for j in range(height)]
        self.history = []
        self.groups = dict()  # {groupID: Group}
        self.affiliation = dict()  # {position: groupID} ease fetching neighb.group
        self.handicap = 0

    def __repr__(self):
        return '\n'.join(str(row) for row in self.board)

    def handicap_stones(self, stones):
        stone_pos = {9: ['7G', '3C', '3G', '7C', '5E'],
                     13: ['10Q', '4D', '4Q', '10D', '7K', '7D', '7Q', '10K', '4K'],
                     19: ['16Q', '4D', '4Q', '16D', '10K', '10D', '10Q', '16K', '4K']}

        if list(self.size.values()) != [19, 19] and \
                list(self.size.values()) != [13, 13] and \
                list(self.size.values()) != [9, 9]:
            raise ValueError('boardsize is not suitable for handicap stones')
        elif len(stone_pos[self.size['height']]) < stones:
            raise ValueError('too many handicap stones for given boardsize')
        elif any(j == 'x' for i in self.board for j in i):
            # TODO: replace this by _groups
            raise ValueError('game has already started or you called handicap_stones twice')
        else:
            ls = [self.parse_position(stone) for stone in stone_pos[self.size['height']][0:stones]]

            self.groups.update(
                {i: Group(firststone=pos, groupID=i, liberties=n,  color='b')
                 for i, pos in enumerate(ls)})
            self.affiliation.update({pos: i for i, pos in enumerate(ls)})

            # white starts to play after handicap
            self.history.append('handicap')
            self.handicap = stones

            # bring black on board
            for r, c in ls:
                self.board[r][c] = 'x'

    # Deprec
    # def _diff_neighb(self, neighb, color):
    #     """find the differntly colored neighbours"""
    #     return [n for n in neighb
    #             if self.board[n[0]][n[1]] == ['x', 'o'][(len(self.history) + 1) % 2]]

    def move(self, *positions):
        """positions may take multiple values:
        move("4A", "5A", "6A")"""
        for position in positions:
            r, c = self.parse_position(position)

            if self._valid_move(r, c, position):
                color = ['x', 'o'][len(self.history) % 2]
                self.board[r][c] = color
                neighb = self._find_neighb(r, c)

                # (0) create new group (single stone) with no affiliation
                # -1 so that it follows the logic of handicap_stones
                groupID = len(self.history) + self.handicap
                self.groups.update({groupID: Group(
                    firststone=(r, c),
                    groupID=groupID,
                    liberties=set(n for n in neighb if n not in self.affiliation.keys()),
                    color=self.turn())})
                self.history.append(position)
                self.affiliation.update({(r, c): groupID})

                # FIXME: check if any group will be removed by capturing!

                # (1) same color (including mid stone)
                self._merge_same_color(neighb, color, groupID, r, c)

                # (2) different colored neighbours: steal liberty
                self._different_color_update(neighb, color, r, c)

    def _merge_same_color(self, neighb, color, groupID, r, c):
        pos_same_col = [n for n in neighb if self.board[n[0]][n[1]] == color]

        if pos_same_col != []:
            # find largest Group (a bit of extra logic for fast moves in mid/end game)
            membersize = [len(self._fetch_group(n).member) for n in pos_same_col]
            pos_max_grsize = pos_same_col[membersize.index(max(membersize))]
            pos_same_col.remove(pos_max_grsize)
            # update with: same_col_no_max=[self._fetch_group_by_pos(n) for n in pos_same_col]
            same_col_nomax = [self.groups[id] for id in [self.affiliation[n] for n in pos_same_col]]
            max_id = self.affiliation[pos_max_grsize]

            # merge to max group
            self.groups[max_id].merge(self.groups[groupID], *same_col_nomax)

            # remove mid (new) stone liberty
            self.groups[max_id].liberties.remove((r, c))

            # change the affiliation of all same colored to val of max group aff.
            for tup in (*chain(*[group.member for group in same_col_nomax]), (r, c)):
                self.affiliation[tup] = max_id  # TODO check affiliation of single stone!

    def _different_color_update(self, neighb, color, r, c):
        # Fixme: no suicide (4 black white in middl)
        pos_diff_col = [n for n in neighb if self.board[n[0]][n[1]] != color
                        and self.board[n[0]][n[1]] != '.']

        if pos_diff_col != []:
            for tup in pos_diff_col:
                group = self._fetch_group(tup)
                group.liberties.remove((r, c))

                # check if group has no liberties
                if not bool(group.liberties):
                    self._capture(group=group)

    def _capture(self, group):
        """remove group when it has no liberty after _different_color_update
        each member's neighbour's group must be added this members position is a
        new liberty of that neighbour's group."""
        color = ['x', 'o']
        color.remove(group.color)
        color = color[0]

        # find neighb. of each member & give them the respective liberty!
        member_neighb = list(map(lambda position: self._find_neighb(*position), group.member))
        diff_group = [set(self._fetch_group(n) for n in neighb if self.board[n[0]][n[1]] == color)
                             for neighb in member_neighb]

        for member, ngroup in zip(group.member, diff_group):
            ngroup.liberties.extend(member)


        for i, pos in enumerate(group.member):
            # remove affiliations of all group member:
            self.affiliation.popitem(pos)

            # remove member from board
            board[pos[0]][pos[1]] = '.'

    def _fetch_group(self, position):
        return self.groups[self.affiliation[position]]

    def _find_neighb(self, r, c):
        cond = lambda r, c: r >= 0 and r < self.size['height'] and c >= 0 and c < self.size['width']
        neighb = [(r + i, c) for i in [-1, 1] if cond(r + i, c)]  # horizontal
        neighb.extend((r, c + j) for j in [-1, 1] if cond(r, c + j))  # vertical
        return neighb

    def parse_position(self, move):
        # TODO: make a dict
        alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        alpha.remove('I')
        hor = alpha[0:self.size['width']]
        ver = [i for i in reversed(range(self.size['height'] + 1))]

        if int(move[0:-1]) not in ver or move[-1] not in hor:
            raise ValueError('You are out of bounds')
        else:
            return ver[int(move[0:-1])], hor.index(move[-1])

    def _valid_move(self, r, c, position):
        #  (1) if stone already @ pos.
        if self.board[r][c] != '.':
            raise ValueError('cannot place a stone on top of another stone')

        # TODO (2.1) if KO was started (placing @ 1st removed stone)

        # (2.2) if KO (ongoing)
        # if self.history[-2] == position:
        #     raise ValueError('Invalid move due to ongoing KO')

        # ToDO check
        #  (3) suicide move (before assigning: check that same colored groups dont die)
        #   what about connecting stones?

        return True

    def turn(self):
        """getter of current Turn color"""
        return ['black', 'white'][len(self.history) % 2]

    def pass_turn(self):
        """player decides not to move"""
        self.history.append('')

    def get_position(self, position):
        """:return: 'x', 'o' or '.'"""
        position = self.parse_position(position)
        i, j = position

        if self.board[i][j] != '.':
            return self.affiliation[position].color
        else:
            return '.'

    def rollback(self, steps):
        '''rollback the last game moves'''
        # CAREFULL with '' in history
        # CAREFULL with removed groups: consider a capture history
        # list((newstone, captured group), ...)
        pass

    def reset(self):  # FIXME: CHECK ME!!!
        # remove all attributes of self
        for name in [k for k in self.__dict__.keys() if k not in ['size', 'handicap']]:
            delattr(self, name)

        # reset groups
        Go._groups = dict()

        # reinstate attributes.
        self.__init__(**self.size)

        # restore handicap
        self.handicap_stones(self.handicap)


if __name__ == '__main__':
    # TODO : debug capturing, particularly look at liberties of all neighbours of
    #  the members of the group. (they should have the member as new liberty

    # check killing criteria
    go = Go(19)
    go.move('6F')
    go.move('6G')
    go.move('6H')
    go.move('1A')
    go.move('5G')
    go.move('2A')
    go.move('7G')

    # check multiple different color linking stone: liberties correct
    go = Go(19)
    # go.handicap_stones(8)
    go.move('2B')
    go.move('10F')
    go.move('3C')
    print(go)
    go.move('2C')

    go.groups[1].member, go.groups[1].liberties
    go.groups[3].member, go.groups[3].liberties
    go.groups[4].member, go.groups[4].liberties

    # check same color merger linking stone
    go = Go(19)
    # go.handicap_stones(8)
    go.move('2B')
    go.move('10F')
    go.move('3C')
    go.move('19F')
    print(go)
    go.move('2C')
    print(go)

    # NOTICE keeping the "old" merged groups is intentional, since this may
    # ease the recovery!
    go.groups[1].member, go.groups[1].liberties
    go.groups[3].member, go.groups[3].liberties
    go.groups[5].member, go.groups[5].liberties

    # check same color group merger
    go = Go(19)
    go.move('2B')
    go.move('10F')
    print(go)
    go.move('3B')

    go.groups[1].member, go.groups[1].liberties

    # check parse_position
    game = Go(4)
    game.parse_position('2B') == (2, 1)
    # game.move('2B', '3D', '2C')

    # check handicap stones & moves + move liberty difference
    go = Go(19)
    go.handicap_stones(8)
    go.move('2B')
    print(go)  # .__repr__()
    go.move('3B')
    print(go)  # .__repr__()

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
