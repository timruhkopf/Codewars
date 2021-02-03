import unittest

from Lift import Lift
from TheLift.Kata_translation import Dinglemouse


class TestTheLift(unittest.TestCase):

    def test_enter_lift(self):
        queue = ((6, 3, 5), (3, 3, 4), (5, 1, 5), (6,), (1,), (), (0,))
        lift = Lift(capacity=5)
        lift.parse_queues(queue)

        # at floor 0:
        lift._enter_lift()
        self.assertEqual(lift.load, [6, 3, 5])
        self.assertEqual(lift.current_load, 3)

        # add people, but care for the capacity constraint!
        lift.current_floor = 1
        lift._enter_lift()
        self.assertEqual(lift.requests['up'][lift.current_floor], [4])

    def test_exit_lift(self):
        queue = ((6, 3, 5), (3, 3, 4), (5, 1, 5), (6,), (1,), (), (0,))

        lift = Lift(capacity=5)
        lift.parse_queues(queue)

        # at floor 0:
        lift._enter_lift()

        lift.current_floor = 3
        lift._exit_lift()
        self.assertEqual(lift.load, [6, 5])

    def test_next_floor(self):
        pass

    def test_move_up(self):
        pass

    def test_move_down(self):
        pass

    def test_move_switch_directions(self):
        pass

    def test_Dinglemouse_interface(self):
        pass

    def test_kata_examples(self):
        tests = [[((), (), (5, 5, 5), (), (), (), ()), [0, 2, 5, 0]],
                 [((), (), (1, 1), (), (), (), ()), [0, 2, 1, 0]],
                 [((), (3,), (4,), (), (5,), (), ()), [0, 1, 2, 3, 4, 5, 0]],
                 [((), (0,), (), (), (2,), (3,), ()), [0, 5, 4, 3, 2, 1, 0]]]

        for queues, answer in tests:
            lift = Dinglemouse(queues, capacity=5)
            self.assertEqual(lift.theLift(), answer)



if __name__ == '__main__':
    unittest.main()
