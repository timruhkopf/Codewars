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
            width == height

        # required attribute
        self.size = {'height': height, 'width': width}

        # TODO: make board property: getter method uses dict representation
        self.board = [['.' for i in range(width)] for j in range(height)]
        # Consider: board = {position:Stone(position)} for ease of fetching neighbours
        position, groupID = None, None
        self.affiliation = {position: groupID}  # dict to keep track of all group members
        # i.e. asking neighbours' groupID here

        self.history = []  # strings of positions e.g. "A7" allows to check invalid
        # KO placements -i.e. player places stone at his turn in the same position
        # he did on his previous turn.
        # self.move_counter = 0 # == len(self.history)

    def handicap_stones(self, stones):
        color = 'b'
        # ToDo Board size dependent and order specific!
        pass

    def move(self, position):
        # ToDo parse position
        x = None  # FIXME
        y = None

        if self._valid_move():
            self.history.append(position)

        # Consider: check neighbours of position and add stone to a group if
        # there exists a stone of same color on cross. BE AWARE of "linking stones"
        neighb = [(x - i, y - j) for i in [-1, 1] for j in [-1, 1]]

        # update affiliation

        # update groups
        # (1) membership
        # (2) liberties union. (same color) (to avoid circular patterns and false counting)
        # different color: difference

        pass

    def _valid_move(self):
        # ToDO check
        #  (1) if stone already @ pos.
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
    pass
