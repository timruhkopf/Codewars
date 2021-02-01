import unittest
from Loopover.Cyclic_shift import Cyclic_shift_board


class TestCyclic_shift(unittest.TestCase):
    def test_Calibration(self):
        #   # # (CALIBRATION TEST) -----------------------------------------------------
        #     # c = Cyclic_shift_board(board('ACDBE\nFGHIJ\nKLMNO\nPQRST'))
        #     # c.shift('L0')
        #     # assert (c.solution[-1] == 'L0')
        #     # c.shift('R0')
        #     # assert (c.solution[-1] == 'R0')
        #     # c.shift('D0')
        #     # assert (c.solution[-1] == 'D0')
        #     # c.shift('U0')
        #     # assert (c.solution[-1] == 'U0')
        pass

    def test_unsolvables(self):
        #  # @test.it('Test 5x5 (unsolvable)')
        #     run_test('WCMDJ\nORFBA\nKNGLY\nPHVSE\nTXQUI',
        #              'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', True)
        #
        #     run_test("""AQYEH BUXKF WVTLP JCDMR IONGS""".replace(' ', '\n'),
        #              """ABCDE FGHIJ KLMNO PQRST UVWXY""".replace(' ', '\n'), True)
        #
        #     # 5x9
        #     run_test("""PBMnj ZVToq JCpLH UeFDR imIfG WKEON csAgr laYhX dQkSb""".replace(' ', '\n'),
        #              """ABCDE FGHIJ KLMNO PQRST UVWXY Zabcd efghi jklmn opqrs""".replace(' ', '\n'), True)
        #
        #     # 9x9
        #     run_test(
        #         """enwξfxWχλ Zh1cv4qωR ρ3TEFψπMJ KmDiεHCγG η7IXA2Uzk 0NβpVB8Yb αuθ6tφdδσ 5LμaOjζsS lyPg9rQνo""".replace(' ',
        #                                                                                                                 '\n'),
        #         """ABCDEFGHI JKLMNOPQR STUVWXYZa bcdefghij klmnopqrs tuvwxyz01 23456789α βγδεζηθλμ νξπρσφχψω""".replace(' ',
        #                                                                                                                 '\n'),
        #         True)
        #
        #     # 7x7
        #     run_test("""dMeuTgG ncfiVZo FJRNbLH OPDEKvj ltXpUhq AWSIQmr kwaYBCs""".replace(' ', '\n'),
        #              """ABCDEFG HIJKLMN OPQRSTU VWXYZab cdefghi jklmnop qrstuvw""".replace(' ', '\n'), True)
        pass

    def test_solve_simple(self):
        # # @test.it('Test 2x2 (1)')
        # run_test('12\n34', '12\n34', False)
        #
        # # @test.it('Test 2x2 (2)')
        # run_test('42\n31', '12\n34', False)

        # # @test.it('Test 5x5 (2)')
        # run_test('ABCDE\nKGHIJ\nPLMNO\nFQRST\nUVWXY',
        #          'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)
        pass

    def test_solve(self):
        # # @test.it('Test 5x5 (3)')
        # run_test('CWMFJ\nORDBA\nNKGLY\nPHSVE\nXTQUI',
        #          'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)
        #
        # # @test.it('Test 6x6')
        # run_test('WCMDJ0\nORFBA1\nKNGLY2\nPHVSE3\nTXQUI4\nZ56789',
        #          'ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789', False)
        pass

    def test_random_tests(self):
        # # 5x5
        # c = Cyclic_shift_board(board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'))
        # c.__repr__()
        # scrambled = c.shuffle(100)
        # c.solve(board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'))

        # # 6x6
        # c = Cyclic_shift_board(board('ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789'))
        # c.shuffle(100)
        # c.solve(board(('ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789')))
        pass

    # (DEBUGBEHAVIOUR) ---------------------------------------------------------
    def test_shift(self):
        pass

    def test_shuffle(self):
        pass

    def test_debug_check(self):
        pass


if __name__ == '__main__':
    unittest.main()
