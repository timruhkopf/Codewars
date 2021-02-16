class Group:
    def __init__(self, firststone, groupID, liberties, color):
        self.member = {firststone}
        self.groupID = groupID
        self.liberties = set(liberties)  # set of positions
        self.color = color

    def merge(self, *others):
        """:param others: iterable of Group instances"""
        self.liberties.update(
            *(lib for lib in (group.liberties for group in others)))
        self.member.update((item for group in others for item in group.member))

    def __hash__(self):  # for set behaviour on values
        return self.groupID
