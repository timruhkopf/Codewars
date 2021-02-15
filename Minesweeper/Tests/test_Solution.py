import unittest


class TestSolution(unittest.TestCase):

    def setUp(self) -> None:
        # result = """
        #    1 x x 1 0 0 0
        #    2 3 3 1 0 1 1
        #    1 x 1 0 0 1 x
        #    1 1 1 0 0 1 1
        #    0 1 1 1 0 0 0
        #    0 1 x 1 0 0 0
        #    0 1 1 1 0 1 1
        #    0 0 0 0 0 1 x
        #    0 0 0 0 0 1 1
        #    """
        # result_board = Solution(board(result))
        pass

    def test_cover_true_board(self):
        # gamemap = """
        #    ? ? ? ? 0 0 0
        #    ? ? ? ? 0 ? ?
        #    ? ? ? 0 0 ? ?
        #    ? ? ? 0 0 ? ?
        #    0 ? ? ? 0 0 0
        #    0 ? ? ? 0 0 0
        #    0 ? ? ? 0 ? ?
        #    0 0 0 0 0 ? ?
        #    0 0 0 0 0 ? ?
        #    """.replace(' ', '')
        # # test open from context works
        # result_board = Solution(board(result))
        # m = Game(board(gamemap), n=result.count('x'), context=result_board)
        # m.open(0, 0)
        # print(m)

        # TODO assert gamemap = covered board
        # TODO check Solution.n is correct
        pass

    def test_sample_boards(self):
        # Todo test random boards

        # sample a board:
        # result_board = Solution()
        # result_board.sample_board(10, dim=(5, 7))
        pass


if __name__ == '__main__':
    unittest.main(exit=False)
