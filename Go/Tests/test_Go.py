import unittest


class TestGo(unittest.TestCase):
    # (A short tutorial on writing Tests) --------------------------------------
    # def setUp(self):
    #     """A optional method, that is called before each test case to factor out
    #      common set up code across test cases"""
    #     self.widget = Widget('The widget')
    #
    # def tearDown(self):
    #     """an optional method, called after each test case"""
    #     self.widget.dispose()
    #
    # def test_function_example(self):
    #     # any test needs to have at least one assert* statement from the following
    #     # https://docs.python.org/3/library/unittest.html#unittest.TestCase
    #     self.assertEqual(True, True)

    def test_board_setup_sizes(self):
        # test.describe("Creating go boards")
        # test.it("9x9")
        # game = Go(9)
        # board = [[".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", "."]]
        # test.assert_equals(game.board, board, "Should generate a 9 by 9 board.")
        # # close_it()
        #
        # test.it("13x13")
        # game = Go(13)
        # board = [[".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]]
        # test.assert_equals(game.board, board, "Should generate a 13 by 13 board.")
        # # close_it()
        #
        # test.it("19x19")
        # game = Go(19)
        # board = [[".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        #          [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]]
        # test.assert_equals(game.board, board, "Should generate a 19 by 19 board.")

        # test.it("32x32")
        # test.expect_error("Should throw an error. Board cannot be larger than 25 by 25", lambda: Go(32))
        # # close_it()
        # # close_describe()
        pass

    def test_handicap(self):
        #
        # # check handicap stones & moves + move liberty difference
        # go = Go(19)
        # go.handicap_stones(8)
        # go.move('2B')
        # print(go)  # .__repr__()
        # go.move('3B')
        # print(go)  # .__repr__()

        # test.describe("Handicap stones")
        # test.it("Three handicap stones on 9x9")
        # game = Go(9)
        # finalBoard = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
        #               ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
        #               ['.', '.', '.', '.', '.', '.', 'x', '.', '.'],
        #               ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
        #               ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
        #               ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
        #               ['.', '.', 'x', '.', '.', '.', 'x', '.', '.'],
        #               ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
        #               ['.', '.', '.', '.', '.', '.', '.', '.', '.']]
        #
        # game.handicap_stones(3)
        # test.assert_equals(game.board, finalBoard)
        # # close_it()
        # # close_describe()

        pass

    def test_reset_board(self):
        # # reset the board:
        # go.reset()
        # print(go)
        # go.handicap
        # go.groups
        # go.affiliation
        # go.size
        pass

    def test_turn(self):
        # color of current turn
        # game = Go(9)
        # game.move("3B")
        # assert game.turn == "white"
        # game.move("4B")
        # assert game.turn == "black"
        pass

    def test_parse_position(self):
        # check parse_position
        # game = Go(4)
        # game.parse_position('2B') == (2, 1)
        # game.move('2B', '3D', '2C')
        pass

    def test_get_position(self):
        # assert game.get_position("9A"), "."  # , "Illegal stone should be removed"
        # game.move("3B")
        # game.get_position("3B"), "x", "Black should have another try"
        pass

    def test_pass_turn(self):
        # test.it("Can pass turn")
        # game = Go(9)
        # game.pass_turn()
        # test.assert_equals(game.turn, "white")
        # # close_it()
        pass


if __name__ == '__main__':
    unittest.main()
