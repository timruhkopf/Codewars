import unittest


class TestMove(unittest.TestCase):
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

    def test_plain(self):
        # test.describe("Placing stones")
        # test.it("Place a black stone")
        # game = Go(9)
        # game.move("3D")
        # test.assert_equals(game.get_position("3D"), "x")
        # # close_it()
        #
        # test.it("Place a white stone")
        # game.move("4D")
        # test.assert_equals(game.get_position("4D"), "o")
        # # close_it()

        pass

    def test_multiple(self):
        # test.it("Can take multiple moves at a time")
        # game.move("4A", "5A", "6A")
        # test.assert_equals(game.get_position("4A"), "x")
        # test.assert_equals(game.get_position("5A"), "o")
        # test.assert_equals(game.get_position("6A"), "x")
        # # close_it()
        pass

    def test_on_top_of_existing_stone(self):
        # test.it("Cannot place a stone on an existing stone. Raises an error.")
        # test.expect_error("3D should be an invalid move", lambda: game.move("3D"))
        # test.expect_error("4D should be an invalid move", lambda: game.move("4D"))
        # # close_it()
        pass

    def test_out_of_bound(self):
        # test.it("Cannot place a stone with out of bounds coordinates. Raises an error.")
        # test.expect_error("3Z should be an invalid move", lambda: game.move('3Z'))
        # test.expect_error("66 should be an invalid move", lambda: game.move('66'))
        # # close_it()
        # # close_describe()
        pass

    def test_reduce_Group_liberties(self):
        # # check multiple different color linking stone: liberties correct
        # go = Go(19)
        # # go.handicap_stones(8)
        # go.move('2B')
        # go.move('10F')
        # go.move('3C')
        # print(go)
        # go.move('2C')
        #
        # go.groups[1].member, go.groups[1].liberties
        # go.groups[3].member, go.groups[3].liberties
        # # go.groups[4].member, go.groups[4].liberties
        pass

    def test_merge_Groups(self):
        # # check same color merger linking stone
        # go = Go(19)
        # # go.handicap_stones(8)
        # go.move('2B')
        # go.move('10F')
        # go.move('3C')
        # go.move('19F')
        # print(go)
        # go.move('2C')
        # print(go)

        # check same color group merger
        # go = Go(19)
        # go.move('2B')
        # go.move('10F')
        # print(go)
        # go.move('3B')
        #
        # go.groups[1].member, go.groups[1].liberties

        pass

    def test_killing_criteria(self):
        # check killing criteria remove a white group with multiple stones
        # TODO make assert statements
        # go = Go(19)
        # moves = ['6F', '6G', '6H', '7G', '5G', '2A', '7F', '1A', '7H', '3A']
        # go.move(*moves)
        # print(go)
        # go.move('8G')
        #
        # go.groups[0].member, go.groups[0].liberties
        # go.groups[2].member, go.groups[2].liberties
        # go.groups[4].member, go.groups[4].liberties
        # go.groups[10].member, go.groups[10].liberties
        #
        # # check killing criteria
        # go = Go(19)
        # go.move('6F')
        # go.move('6G')
        # go.move('6H')
        # go.move('1A')
        # go.move('5G')
        # go.move('2A')
        # print(go)
        # go.move('7G')
        # print(go)
        #
        # go.groups[0].member, go.groups[0].liberties
        # go.groups[2].member, go.groups[2].liberties
        # go.groups[4].member, go.groups[4].liberties
        # go.groups[6].member, go.groups[6].liberties
        pass

    def test_capture(self):
        pass

    def test_corner_capture(self):
        # test.it("Corner capture")
        # game = Go(9)
        # moves = ["9A", "8A", "8B", "9B"]
        # game.move(*moves)
        # test.assert_equals(game.get_position('9A'), ".")
        # # close_it()
        pass

    def test_multi_capture(self):
        # # multiple captures:
        # game = Go(9)
        # moves = ["5D", "5E", "4E", "6E", "7D", "4F", "7E", "3E", "5F", "4D",
        #          "6F", "6D", "6C", "7F", "4E", "5E"]
        # captured = ["4E", "6D", "6E"]
        # game.move(*moves)
        # for capture in captured:
        #     assert game.get_position(capture), "."
        #
        # # multiple stone capture
        # game = Go(9)
        # moves = ["6D", "7E", "6E", "6F", "4D", "5E", "5D", "7D",
        #          "5C", "6C", "7H", "3D", "4E", "4F", "3E", "2E",
        #          "3F", "3G", "2F", "1F", "2G", "2H", "1G", "1H"]
        # game.move(*moves)
        # print(game)
        #
        # game.move(*["4C", "3C", "6H", "4B", "5H", "5B"])
        # captured = ["6D", "6E", "4D", "5D", "5C", "4E", "3E", "3F", "2F", "2G", "1G", "4C"]
        #
        # for capture in captured:
        #     assert game.get_position(capture), "."
        #
        pass

    def test_elongateGroup(self):
        pass

    def test_ko(self):
        # KO
        # go = Go(5)
        # moves = ["5C", "5B", "4D", "4A", "3C", "3B",
        #          "2D", "2C", "4B", "4C"]
        # go.move(*moves)
        # print(go)
        # TODO works just fine, but needs a expect error
        # go.move("4B")
        # go.move("2B")
        pass

    def test_snapback(self):
        # # "Snapback"
        # game = Go(5)
        # moves = ["5A", "1E", "5B", "2D", "5C", "2C", "3A",
        #          "1C", "2A", "3D", "2B", "3E", "4D", "4B",
        #          "4E", "4A", "3C", "3B", "1A", "4C"]
        # captured = ["4A", "4B", "4C", "3B"]
        # game.move(*moves)
        # game.move("3C")
        # for capture in captured:
        #     assert game.get_position(capture), "."

        pass

    def test_suicide(self):
        ##  "Self-capturing throws an error.")
        # game = Go(9)
        # moves = ["4H", "8A", "8B", "9B"]
        # game.move(*moves)
        # print(game)
        # # TODO expect error:
        # game.move("9A")
        pass


if __name__ == '__main__':
    unittest.main()
