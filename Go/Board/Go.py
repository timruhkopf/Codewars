from .Group import Group
from ..Strategies.StrategyMove import StrategyMove


class Go:
    def __init__(self, height, width=None):
        """
        TODO add doc
        https://www.codewars.com/kata/59de9f8ff703c4891900005c"""
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
        self.capured = dict()  # {len(history at capture): captured members}

        self.parse_position = self._precompute_for_parsing()

    def __repr__(self):
        return '\n'.join(str(row) for row in self.board)

    # (Internal methods) -------------------------------------------------------
    def _occupied(self, r, c):
        """returns true if no stone @ the requested position pos."""
        if self.board[r][c] != '.':
            raise ValueError('cannot place a stone on top of another stone')
        return True

    def _fetch_group(self, position):
        """return the instance of a group by position"""
        return self.groups[self.affiliation[position]]

    def _find_neighb(self, r, c):
        """:return list of position tuples, representing
        horizontal vertical adjacent positions"""
        cond = lambda r, c: r >= 0 and r < self.size['height'] and c >= 0 and c < self.size['width']
        neighb = [(r + i, c) for i in [-1, 1] if cond(r + i, c)]  # horizontal
        neighb.extend((r, c + j) for j in [-1, 1] if cond(r, c + j))  # vertical
        return neighb

    def _precompute_for_parsing(self):
        """decorator to precompute the indicies for parsing only once in self.__init__"""
        alpha = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        alpha.remove('I')
        hor = alpha[0:self.size['width']]
        ver = [i for i in reversed(range(self.size['height'] + 1))]

        def parse_position(move):
            if int(move[0:-1]) not in ver or move[-1] not in hor:
                raise ValueError('You are out of bounds')
            else:
                return ver[int(move[0:-1])], hor.index(move[-1])

        return parse_position

    # (playable methods) -------------------------------------------------------
    def handicap_stones(self, stones):
        """todo add doc"""
        stone_pos = {9: ['7G', '3C', '3G', '7C', '5E'],
                     13: ['10K', '4D', '4K', '10D', '7G', '7D', '7K', '10G', '4G'],
                     19: ['16Q', '4D', '4Q', '16D', '10K', '10D', '10Q', '16K', '4K']}

        if list(self.size.values()) != [19, 19] and \
                list(self.size.values()) != [13, 13] and \
                list(self.size.values()) != [9, 9]:
            raise ValueError('boardsize is not suitable for handicap stones')
        elif len(stone_pos[self.size['height']]) < stones:
            raise ValueError('too many handicap stones for given boardsize')
        elif len(self.history) != 0:
            raise ValueError('game has already started or you called handicap_stones twice')
        else:
            ls = [self.parse_position(stone) for stone in stone_pos[self.size['height']][0:stones]]

            self.groups.update(
                {i: Group(firststone=pos, groupID=i, liberties=self._find_neighb(*pos), color='x')
                 for i, pos in enumerate(ls)})
            self.affiliation.update({pos: i for i, pos in enumerate(ls)})

            # white starts to play after handicap
            self.history.append('handicap')
            self.handicap = stones

            # place handicap stones
            for r, c in ls:
                self.board[r][c] = 'x'

    def move(self, *positions):
        """todo add more extensive doc
        positions may take multiple values: move("4A", "5A", "6A")"""
        StrategyMove.execute_move(self, *positions)

    # Kata's required methods ------------------------
    @property
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

        return self.board[i][j]

    def rollback(self, steps):
        """rollback the last game moves (by replaying the history)"""
        if len(self.history) < steps:
            raise ValueError('invalid rollback to few moves to unravel')

        history = self.history
        handicap = self.handicap

        # reinstate attributes.
        self.__init__(**self.size)

        # restore handicap
        if handicap != 0:
            self.handicap_stones(handicap)
            history = history[1:]

        for m in history[:-steps]:
            if bool(m):
                self.move(m)
            else:
                self.pass_turn()

    def reset(self):
        """remove all stones of the board"""
        self.__init__(**self.size)
