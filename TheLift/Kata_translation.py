from TheLift.Lift import Lift


class Dinglemouse(object):

    def __init__(self, queues, capacity):
        """
        This class is the target format to the kata. I don't like the design,
        so this is a translation to meet the kata's requirements.
        """
        self.lift = Lift(capacity=capacity)
        self.lift.parse_queues(queues)

    def theLift(self):
        self.lift.move()
        return self.lift.visited
