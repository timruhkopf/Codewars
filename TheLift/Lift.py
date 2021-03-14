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

        # only when activated, the state switches!
        self.switch_state(StateUP(self))

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
        self.requests = {'up': up, 'down': list(reversed(down))}

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

        self._enter_lift()  # enter lift in floor zero if any!
        while self.current_load > 0 or \
                any([*self.requests['down'], *self.requests['up']]):  # any more requests,  # lazy eval!
            self.current_floor = self.next_floor
            self._exit_lift()
            self._enter_lift()  # works with 0 people entering!

        self.switch_state(state=StateUP(self))


# State pattern: https://refactoring.guru/design-patterns/state/python/example
class StateUP:
    heading = 'up'

    def __init__(self, lift):
        self.lift = lift
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
            # default aleviates min([]) error - and the (now existing) next_request
            # will always be smaller than height!
            return min([min(self.lift.load, default=self.lift.height), next_request])

        except StopIteration:
            self.lift.switch_state(self.next_state(self))

            if any(self.lift.requests['down']):
                # go to highest down request  -'smart' strategy
                return next(self.lift.height - f for f, queue in enumerate(self.lift.requests['down']) if bool(queue))

            elif any(self.lift.requests['up']):
                # smallest up request
                return next(f for f, queue in enumerate(self.lift.requests['up']) if bool(queue))

            else:
                return 0


class StateDown:
    heading = 'down'

    def __init__(self, lift):
        self.lift = lift
        self.next_state = StateUP

    @property
    def next_floor(self):

        # ordered down_requests
        down_requests = (self.lift.current_floor - f for f, queue in enumerate(self.lift.requests['down'])
                         if bool(queue) and f < self.lift.current_floor)
        try:
            next_request = next(down_requests)
            # default alleviates min([]) error - and 0 will always be
            # smaller than the (now existing) next_request!
            return max([max(self.lift.load, default=0), next_request])

        except StopIteration:
            if any(self.lift.requests['up']):
                self.lift.switch_state(self.next_state(self))
                return self.lift._state.next_floor

            elif any(self.lift.requests['down']):  # 'smart' strategy
                # topmost down request
                return next(f for f, queue in enumerate(list(reversed(self.lift.requests['down']))) if bool(queue))

            else:
                return 0


if __name__ == '__main__':
    ((3, 3, 3, 3, 3, 3), (), (), (), (), (4, 4, 4, 4, 4, 4), ()), 5
