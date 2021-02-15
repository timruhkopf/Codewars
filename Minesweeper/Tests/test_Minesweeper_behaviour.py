import unittest


class Test_Minesweeper_behaviour(unittest.TestCase):

    def test_state_map(self):
        pass

    def test_state_recursion(self):
        """test how a position's update causes the next to update"""
        pass

    def test_state_found_bomb(self):
        """testing communicate_bombs function & found bomb"""
        pass

    def test_state_equal_qb(self):
        """the number of bombs and the number of question marks is same after state update"""
        pass

    def test_state_hitting0(self):
        """when a state update reveals the last bomb all remaining "?" neighbours
         are clear to open."""
        pass


if __name__ == '__main__':
    unittest.main(exit=False)
