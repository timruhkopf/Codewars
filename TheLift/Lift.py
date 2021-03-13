# FIXME: The kata requires the lift to stop at every! floor in a direction (including those
#  that want to go into the opposite direction? -- > in this case, the split in up and down requests is no longer
#  necessary - instead, next floor is the next non empty floor into a direction until there are no non-empty in that
#  direction -- then the lift must change direction!

class Lift:
    def __init__(self, capacity, height=None):
        """
        https://www.codewars.com/kata/58905bfa1decb981da00009e
        """
        self.capacity = capacity
        self.height = height  # of building
        self.load = []
        self._state = None
        self.visited = [0]

    @property
    def heading(self):
        return self._state.heading

    @property
    def current_load(self):
        return len(self.load)

    @property
    def current_floor(self):
        return self.visited[-1]

    @current_floor.setter
    def current_floor(self, v):
        self.visited.append(v)

    @property
    def next_floor(self):
        # part of the state pattern
        # "When called, the Lift will stop at a floor even if it is full":
        # to avoid sorting lift at each floor to determine the next floor to visit
        # min(self.load)/ max(self.load) are used!
        return self._state.next_floor

    def parse_queues(self, queue):
        """TODO make up and down FIFO queue.Priority_queue objects for a
            real life example with dynamic requests"""
        self.height = len(queue)

        up = [[person for person in v if person > floor] for floor, v in enumerate(queue)]
        down = [[person for person in v if person < floor] for floor, v in enumerate(queue)]
        self.requests = {'up': up, 'down': down}

        # only when activated, the state switches!
        self.switch_state(StateUP(self))

    def switch_state(self, state):
        self._state = state

    def _exit_lift(self):
        # remove all those passengers with the same floor number
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

    def move(self):
        """
        The Lift never changes direction until there are no more people wanting
        to get on/off in the direction it is already travelling When empty the
        Lift tries to be smart. For example, If it was going up then it may
        continue up to collect the highest floor person wanting to go down If it
        was going down then it may continue down to collect the lowest floor
        person wanting to go up.
        """
        any_more_requests = lambda: any(bool(floor) for direct in ['up', 'down']
                                        for floor in self.requests[direct])

        self._enter_lift()
        while self.current_load > 0 or any_more_requests():  # lazy eval!
            self.current_floor = self.next_floor
            self._exit_lift()
            self._enter_lift()  # works with 0 people entering!
            self._state.check_end_ofthe_line()

        else:
            # If the lift is empty, and no people are waiting, then it will return to the ground floor
            self.current_floor = 0
            self.switch_state(state=StateUP())


# State pattern: https://refactoring.guru/design-patterns/state/python/example
class StateUP:
    heading = 'up'

    def __init__(self, lift):
        self.lift = lift
        self.default = lift.height
        self.next_state = StateDown

    @property
    def next_floor(self):
        # - next in load or next non empty floor requesting to go in the same direction
        # - When called, the Lift will stop at a floor even if it is full, although
        #   unless somebody gets off nobody else can get on!
        up_requests = (f for f, queue in enumerate(self.lift.requests['up'])
                       if bool(queue) and f > self.lift.current_floor)
        try:
            next_request = next(up_requests)
        except StopIteration:
            # continue up to the highest person wanting to go down

            # move this to
            next_request = next((f for f, queue in
                                 zip(range(self.lift.current_floor + 1, self.lift.height - 1),
                                     self.lift.requests['down'][self.lift.current_floor + 1:])
                                 if bool(queue)))

            self.lift.switch_state(self.next_state(self))
        else:
            return min([min(self.lift.load, default=self.default), next_request])

    def check_end_ofthe_line(self):
        # no up requests, that are higher than current ("smart" strategy)
        if not any(bool(floor) for floor in self.requests):
            self.lift.switch_state(self.next_state(self.lift))


class StateDown(StateUP):
    heading = 'down'
    default = 0

    def __init__(self, lift):
        self.lift = lift
        self.next_state = StateUP

    @property
    def next_floor(self):
        # - next in load or next non empty floor requesting to go in the same direction
        # - When called, the Lift will stop at a floor even if it is full, although
        #   unless somebody gets off nobody else can get on!
        up_requests = (f for f, queue in enumerate(self.lift.requests['down'])
                       if bool(queue) and f < self.lift.current_floor)
        try:
            next_request = next(up_requests)
        except StopIteration:
            # continue up to the highest person wanting to go down

            # move this to
            next_request = next((f for f, queue in
                                 zip(range(self.lift.current_floor + 1, self.lift.height - 1),
                                     self.lift.requests['up'][self.lift.current_floor + 1:])
                                 if bool(queue)))

            self.lift.switch_state(self.next_state(self))
        else:
            return min([min(self.lift.load, default=self.default), next_request])

    # @property
    # def requests(self):
    #     return self.lift.requests[self.heading][:self.lift.current_floor - 1]

    # @property
    # def next_floor(self):
    #     # - next in load or next non empty floor requesting to go in the same direction
    #     # - When called, the Lift will stop at a floor even if it is full, although
    #     #   unless somebody gets off nobody else can get on!
    #
    #     # the next lower floor request
    #     headed_requests = (f for f, queue in reversed(zip(range(self.lift.current_floor - 1), self.requests))
    #                        if bool(queue))
    #     return min([min(self.lift.load, default=self.default), next(headed_requests)])  # FIXME: must be MAX!


if __name__ == '__main__':
    ((3, 3, 3, 3, 3, 3), (), (), (), (), (4, 4, 4, 4, 4, 4), ()), 5

    lift.move()
