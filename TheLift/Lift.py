class Lift:
    def __init__(self, capacity, height=None):
        """
        https://www.codewars.com/kata/58905bfa1decb981da00009e
        """
        self.capacity = capacity
        self.height = height  # of building
        self.load = []
        self.heading = 'up'
        self.visited = [0]

    @property
    def current_load(self):
        # just for expressiveness
        return len(self.load)

    @property
    def current_floor(self):
        return self.visited[-1]

    @current_floor.setter
    def current_floor(self, v):
        self.visited.append(v)
        self.current_floor = 1

    @property
    def next_floor(self):
        # "When called, the Lift will stop at a floor even if it is full":
        # to avoid sorting lift at each floor to determine the next floor to visit
        # min(self.load)/ max(self.load) are used!
        if self.heading == 'up':
            # next in load or next non empty floor requesting to go in the same direction
            up_requests = (f for f, queue in enumerate(self.requests[self.heading][self.current_floor:]) if f)
            next_floor = min(min(self.load), next(up_requests))

        else:  # down
            up_requests = (f for f, queue in enumerate(self.requests[self.heading][:self.current_floor]) if f)
            next_floor = max(max(self.load), next(up_requests))

        return next_floor

    def parse_queues(self, queue):
        """TODO make up and down FIFO queue.Priority_queue objects for a
            real life example with dynamic requests"""
        self.height = len(queue)

        up = [[person for person in v if person > floor] for floor, v in enumerate(queue)]
        down = [[person for person in v if person < floor] for floor, v in enumerate(queue)]
        self.requests = {'up': up, 'down': down}

    def _exit_lift(self):
        self.load = [v for v in self.load if v != self.current_floor]

    def _enter_lift(self):
        """
        People are in "queues" that represent their order of arrival to wait for the Lift
        Only people going the same direction as the Lift may enter it
        Entry is according to the "queue" order, but those unable to enter do not block those behind them
        """
        if self.current_load < self.capacity:
            queue = self.requests[self.heading][self.current_floor]
            entering = min(len(queue), self.capacity - self.current_load)
            self.load.extend(queue[: entering])
            del queue[0:entering]

    def move_up(self):
        """
        CONSIDER State pattern: https://refactoring.guru/design-patterns/state/python/example
        """

        # TODO generalise to to down! (same strategy only different values to care for and reversed)
        # TODO when to switch

        # The Lift never changes direction until there are no more people wanting to get on/off in the direction it
        # is already travelling When empty the Lift tries to be smart. For example, If it was going up then it may
        # continue up to collect the highest floor person wanting to go down If it was going down then it may
        # continue down to collect the lowest floor person wanting to go up
        more_requests = lambda: any(bool(floor) for direct in ['up', 'down']
                                    for floor in self.requests[direct])

        while self.current_load > 0 and more_requests():
            self.current_floor = self.next_floor  # TODO check if this is sufficient to get this behaviour?
            self._exit_lift()
            self._enter_lift()
        else:
            # If the lift is empty, and no people are waiting, then it will return to the ground floor
            self.current_floor = 0


if __name__ == '__main__':
    queue = ((6, 3, 5), (3, 3, 4), (5, 1, 5), (6,), (1,), (), (0,))

    lift = Lift(capacity=5)
    lift.parse_queues(queue)

    # Test enter_lift ---------
    # at floor 0:
    lift._enter_lift()
    assert lift.load == [6, 3, 5]
    assert lift.current_load == 3

    lift.current_floor = 3
    lift._exit_lift()
    assert lift.load == [6, 5]
