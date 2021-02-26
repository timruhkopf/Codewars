import unittest

from ..Board.Go import Go


class TestMove(unittest.TestCase):

    def test_plain(self):
        # test.describe("Placing stones")
        # test.it("Place a black stone")
        game = Go(9)
        game.move("3D")
        self.assertEqual(game.get_position("3D"), "x")

        # test.it("Place a white stone")
        game.move("4D")
        self.assertEqual(game.get_position("4D"), "o")

    def test_multiple(self):
        game = Go(9)
        # test.it("Can take multiple moves at a time")
        game.move("4A", "5A", "6A")
        self.assertEqual(game.get_position("4A"), "x")
        self.assertEqual(game.get_position("5A"), "o")
        self.assertEqual(game.get_position("6A"), "x")

    def test_on_top_of_existing_stone(self):
        game = Go(9)
        game.move("3D")
        with self.assertRaises(ValueError):
            game.move("3D")
        # test.it("Cannot place a stone on an existing stone. Raises an error.")

    def test_out_of_bound(self):
        # test.it("Cannot place a stone with out of bounds coordinates. Raises an error.")
        game = Go(3)
        with self.assertRaises(ValueError):
            game.move("4A")

        with self.assertRaises(ValueError):
            game.move("2D")

    def test_reduce_Group_liberties(self):
        # check multiple different color linking stone: liberties correct
        go = Go(10)
        go.move('2B')
        go.move('3C')
        go.move('2C')  # creates a group

        go.groups[1].member
        self.assertEqual(len(go.groups[1].liberties), 3)  # white stone's liberties are reduced

        go.groups[0].member
        self.assertEqual(len(go.groups[0].liberties), 5)

    def test_merge_Groups(self):
        # check same color merger linking stone
        go = Go(19)

        go.move('2B')
        go.move('10F')
        go.move('3C')
        go.move('19F')
        print(go)
        go.move('2C')
        print(go)

        self.assertTrue(go._fetch_group(go.parse_position('2B')) == go._fetch_group(go.parse_position('2C')) == \
                        go._fetch_group(go.parse_position('3C')))

        # check same color group merger
        go = Go(19)
        go.move('2B')
        go.move('10F')
        print(go)
        go.move('3B')

        blackgroup = go._fetch_group(go.parse_position('3B'))
        self.assertEqual(len(blackgroup.member), 2)
        self.assertEqual(len(blackgroup.liberties), 6)
        self.assertEqual(blackgroup.liberties, {(16, 2), (17, 2), (18, 1), (16, 0), (17, 0), (15, 1)})

    def test_killing_criteria(self):
        # check killing criteria remove a white group with multiple stones
        go = Go(19)
        moves = ['6F', '6G', '6H', '7G', '5G', '2A', '7F', '1A', '7H', '3A']
        go.move(*moves)
        print(go)
        go.move('8G')

        self.assertEqual((go.groups[0].member, go.groups[0].liberties),
                         ({(12, 5), (13, 5)}, {(12, 4), (12, 6), (13, 4), (13, 6), (11, 5), (14, 5)}))
        self.assertEqual((go.groups[2].member, go.groups[2].liberties),
                         ({(12, 7), (13, 7)}, {(13, 8), (11, 7), (12, 6), (13, 6), (14, 7), (12, 8)}))
        self.assertEqual((go.groups[4].member, go.groups[4].liberties),
                         ({(14, 6)}, {(14, 7), (15, 6), (13, 6), (14, 5)}))
        self.assertEqual((go.groups[10].member, go.groups[10].liberties),
                         ({(11, 6)}, {(11, 7), (12, 6), (10, 6), (11, 5)}))

        # check killing criteria
        go = Go(19)
        go.move('6F')
        go.move('6G')
        go.move('6H')
        go.move('1A')
        go.move('5G')
        go.move('2A')
        print(go)
        go.move('7G')
        print(go)
        #
        self.assertEqual((go.groups[0].member, go.groups[0].liberties),
                         ({(13, 5)}, {(13, 4), (13, 6), (12, 5), (14, 5)}))
        self.assertEqual((go.groups[2].member, go.groups[2].liberties),
                         ({(13, 7)}, {(13, 8), (14, 7), (12, 7), (13, 6)}))
        self.assertEqual((go.groups[4].member, go.groups[4].liberties),
                         ({(14, 6)}, {(14, 7), (15, 6), (13, 6), (14, 5)}))
        self.assertEqual((go.groups[6].member, go.groups[6].liberties),
                         ({(12, 6)}, {(12, 5), (12, 7), (13, 6), (11, 6)}))

    def test_corner_capture(self):
        # test.it("Corner capture")
        game = Go(9)
        moves = ["9A", "8A", "8B", "9B"]
        game.move(*moves)
        self.assertEqual(game.get_position('9A'), ".")

    def test_single_capture(self):
        game = Go(9)
        moves = ["5D", "5E", "4E", "6E", "7D", "4F", "7E", "3E", "5F"]
        game.move(*moves)

        # capture
        game.move("4D")
        self.assertEqual(game.get_position('4E'), ".")

    def test_multi_capture(self):
        # multiple captures:
        game = Go(9)
        moves = ["5D", "5E", "4E", "6E", "7D", "4F", "7E", "3E", "5F", "4D",
                 "6F", "6D", "6C", "7F", "4E", "5E"]
        captured = ["4E", "6D", "6E"]

        game.move(*moves)

        final_board = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['.', '.', '.', 'x', 'x', 'o', '.', '.', '.'],
                       ['.', '.', 'x', '.', '.', 'x', '.', '.', '.'],
                       ['.', '.', '.', 'x', 'o', 'x', '.', '.', '.'],
                       ['.', '.', '.', 'o', '.', 'o', '.', '.', '.'],
                       ['.', '.', '.', '.', 'o', '.', '.', '.', '.'],
                       ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['.', '.', '.', '.', '.', '.', '.', '.', '.']]

        self.assertEqual(game.board, final_board)

        # multiple stone capture (huge group
        game = Go(9)
        moves = ["6D", "7E", "6E", "6F", "4D", "5E", "5D", "7D",
                 "5C", "6C", "7H", "3D", "4E", "4F", "3E", "2E",
                 "3F", "3G", "2F", "1F", "2G", "2H", "1G", "1H"]
        game.move(*moves)

        game.move(*["4C", "3C", "6H", "4B", "5H", "5B"])
        captured = ["6D", "6E", "4D", "5D", "5C", "4E", "3E", "3F", "2F", "2G", "1G", "4C"]

        final_board = [['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['.', '.', '.', 'o', 'o', '.', '.', 'x', '.'],
                       ['.', '.', 'o', '.', '.', 'o', '.', 'x', '.'],
                       ['.', 'o', '.', '.', 'o', '.', '.', 'x', '.'],
                       ['.', 'o', '.', '.', '.', 'o', '.', '.', '.'],
                       ['.', '.', 'o', 'o', '.', '.', 'o', '.', '.'],
                       ['.', '.', '.', '.', 'o', '.', '.', 'o', '.'],
                       ['.', '.', '.', '.', '.', 'o', '.', 'o', '.']]

        self.assertEqual(game.board, final_board)

    def test_ko(self):
        go = Go(5)
        moves = ["5C", "5B", "4D", "4A", "3C", "3B",
                 "2D", "2C", "4B", "4C"]
        go.move(*moves)

        # illegal Ko move
        with self.assertRaises(ValueError):
            go.move("4B")

    def test_snapback(self):
        # "Snapback"
        # white captures black group, but is snapped back (no ko)
        game = Go(5)
        moves = ["5A", "1E", "5B", "2D", "5C", "2C", "3A",
                 "1C", "2A", "3D", "2B", "3E", "4D", "4B",
                 "4E", "4A", "3C", "3B", "1A", "4C"]

        captured = ["4A", "4B", "4C", "3B"]
        game.move(*moves)

        # snapback move
        game.move("3C")
        for capture in captured:
            assert game.get_position(capture), "."

    def test_suicide(self):
        #  "Self-capturing throws an error.")
        game = Go(9)
        moves = ["4H", "8A", "8B", "9B"]
        game.move(*moves)
        with self.assertRaises(ValueError):
            game.move("9A")


if __name__ == '__main__':
    unittest.main()
