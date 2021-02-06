import unittest

from Loopover.Board.Cyclic_shift import Cyclic_shift_board, loopover
from Loopover.Board.Cyclic_shift_debug import board


def check_solved(self, base_board, solved_board_True):
    c = Cyclic_shift_board(base_board)
    solution = c.solve(solved_board_True)

    d = Cyclic_shift_board(base_board)
    for direction in solution:
        d.shift(direction)
    solved_board = d.__repr__().replace(' ', '')
    self.assertEqual(solved_board_True, board(solved_board))


class Test_Cyclic_shift(unittest.TestCase):
    def test_Calibration_RowShift(self):
        """check that the playable behavior of the board works as expected"""
        board = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'J'],
            ['K', 'L', 'M', 'N', 'O'],
            ['P', 'Q', 'R', 'S', 'T']]
        c = Cyclic_shift_board(board)

        c.shift('L0')
        self.assertEqual(c.solution[-1], 'L0')
        c.shift('U0')
        self.assertEqual(c.solution[-1], 'U0')
        c.shift('R0')
        self.assertEqual(c.solution[-1], 'R0')
        c.shift('D0')
        self.assertEqual(c.solution[-1], 'D0')

        self.assertEqual(c.solution, ['L0', 'U0', 'R0', 'D0'])
        self.assertEqual(c.__repr__(), 'B F C D E\nA G H I J\nK L M N O\nP Q R S T')

    def test_Calibration_DebugShift(self):
        """testing Debugbehaviour.shift does the exact same thing as Row.shift"""
        board = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'J'],
            ['K', 'L', 'M', 'N', 'O'],
            ['P', 'Q', 'R', 'S', 'T']]
        c = Cyclic_shift_board(board)

        c.rows[0].shift(-1)  # L0
        c.cols[0].shift(1)  # U0
        c.rows[0].shift(1)  # R0
        c.cols[0].shift(-1)  # D0

        self.assertEqual(c.solution, ['L0', 'U0', 'R0', 'D0'])
        self.assertEqual(c.__repr__(), 'B F C D E\nA G H I J\nK L M N O\nP Q R S T')

    def test_solve_simple(self):
        check_solved(self, board('12\n34'), board('12\n34'))
        check_solved(self, board('42\n31'), board('12\n34'))
        check_solved(self, board('ABCDE\nKGHIJ\nPLMNO\nFQRST\nUVWXY'),
                     board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'))

    def test_solve(self):
        # 5 x 5
        base_board = board('CWMFJ\nORDBA\nNKGLY\nPHSVE\nXTQUI')
        solved_board_True = board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY')
        check_solved(self, base_board, solved_board_True)

        # # @test.it('Test 6x6')
        base_board = board('WCMDJ0\nORFBA1\nKNGLY2\nPHVSE3\nTXQUI4\nZ56789')
        solved_board_True = board('ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789')
        check_solved(self, base_board, solved_board_True)

    def test_unsolvables(self):
        # @test.it('Test 5x5 (unsolvable)')
        c = Cyclic_shift_board(board('WCMDJ\nORFBA\nKNGLY\nPHVSE\nTXQUI'))
        self.assertIsNone(c.solve(board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY')))

        # 5 x 5
        c = Cyclic_shift_board(board("""AQYEH BUXKF WVTLP JCDMR IONGS""".replace(' ', '\n')))
        self.assertIsNone(c.solve(board("""ABCDE FGHIJ KLMNO PQRST UVWXY""".replace(' ', '\n'))))

        # 5 x 9
        c = Cyclic_shift_board(board("""PBMnj ZVToq JCpLH UeFDR imIfG WKEON csAgr laYhX dQkSb""".replace(' ', '\n')))
        self.assertIsNone(
            c.solve(board("""ABCDE FGHIJ KLMNO PQRST UVWXY Zabcd efghi jklmn opqrs""".replace(' ', '\n'))))

        # 7 x 7
        c = Cyclic_shift_board(board("""dMeuTgG ncfiVZo FJRNbLH OPDEKvj ltXpUhq AWSIQmr kwaYBCs""".replace(' ', '\n')))
        self.assertIsNone(
            c.solve(board("""ABCDEFG HIJKLMN OPQRSTU VWXYZab cdefghi jklmnop qrstuvw""".replace(' ', '\n'))))

        # 9 x 9
        c = Cyclic_shift_board(board(
            """enwξfxWχλ Zh1cv4qωR ρ3TEFψπMJ KmDiεHCγG η7IXA2Uzk 0NβpVB8Yb αuθ6tφdδσ 5LμaOjζsS lyPg9rQνo""".replace(' ',
                                                                                                                    '\n')))
        self.assertIsNone(
            c.solve(board(
                """ABCDEFGHI JKLMNOPQR STUVWXYZa bcdefghij klmnopqrs tuvwxyz01 23456789α βγδεζηθλμ νξπρσφχψω""".replace(
                    ' ', '\n'))))

    def test_random_tests6x6(self):
        # 6 x 6
        b = 'ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789'
        base_board = board(b)
        for repeat in range(5):

            c = Cyclic_shift_board(base_board)
            scrambled = c.shuffle(10)
            c.solution = []
            solution = c.solve(base_board)

            d = Cyclic_shift_board(board(scrambled))
            for direction in solution:
                d.shift(direction)

            solved_board = d.__repr__().replace(' ', '')
            self.assertEqual(b, solved_board)

    def test_kata_interface(self):
        # DEBUG INTERFACE: The kata requires a loopover function

        #  run_test & board these function was copied and adjusted from the
        #  kata's tests to emulate the behaviour. With unittests, this is obsolete
        #  and unnecessary tedious.
        def run_test(start, end, unsolvable):

            # print_info(board(start), board(end))
            moves = loopover(board(start), board(end))
            if unsolvable:
                self.assertIsNone(moves)  # 'Unsolvable configuration

            else:
                moves = tuple(moves)
                self.assertEqual(Cyclic_shift_board(board(start)).debug_check(moves, board(end)), True)

        run_test('CWMFJ\nORDBA\nNKGLY\nPHSVE\nXTQUI',
                 'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

        run_test('WCMDJ\nORFBA\nKNGLY\nPHVSE\nTXQUI',
                 'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', True)

    def test_transpose_cases(self):
        """all of these should be solvable"""

        # OBSERVATION: always uneven x even. meaning, that if toprow cannot
        # produce any viable solution graph (compare choose_sort_strategy)
        # the first column might  - i.e. lift shift all but the first column
        # and do toprow on the first column.

        # 1) 7x 4
        p1 = """AXUCWYH
        RLSOMbB
        JIGTNFP
        ZQVEaDK"""

        s1 = """ABCDEFG
        HIJKLMN
        OPQRSTU
        VWXYZab"""

        # 2) 9 x 4
        p2 = """JZNGeMFaD
        cPQfYTViK
        gEBbhjRUd
        LISOHXCAW"""

        s2 = """ABCDEFGHI
        JKLMNOPQR
        STUVWXYZa
        bcdefghij"""

        # 3) 7 x 4
        p3 = """VFYEHWG
        BTKAUJS
        IaOLRCZ
        bPDNQMX"""

        s3 = """ABCDEFG
        HIJKLMN
        OPQRSTU
        VWXYZab"""

        # 4) 7 x 8
        p4 = """JqQxXeN
        ErLId2p
        olWcig3
        tTUMnRs
        ZVGyawk
        j0AzbF1
        DBYSCPm
        fvHKOuh"""

        s4 = """ABCDEFG
        HIJKLMN
        OPQRSTU
        VWXYZab
        cdefghi
        jklmnop
        qrstuvw
        xyz0123"""

        # 5) 3 x 4
        p5 = """EFA
        IBC
        GDK
        HLJ"""

        s5 = """ABC
        DEF
        GHI
        JKL"""

        # 6) 7 x 8
        p6 = """jSWkCbY
        hwOzpiL
        dvF3Jgr
        qltBcm1
        MRZsEHa
        eInAfKQ
        XoPTxGU
        DVyuN20"""

        s6 = """ABCDEFG
        HIJKLMN
        OPQRSTU
        VWXYZab
        cdefghi
        jklmnop
        qrstuvw
        xyz0123"""

        # 7) 7 x4
        p7 = """CNHLSYT
        AUJEXBa
        WODRbPK
        QIVFGMZ"""

        s7 = """ABCDEFG
        HIJKLMN
        OPQRSTU
        VWXYZab"""

        for p, s in zip([p1, p2, p3, p4, p5, p6, p7],
                        [s1, s2, s3, s4, s5, s6, s7]):
            p = board(p.replace(' ', ''))
            s = board(s.replace(' ', ''))

            check_solved(self, p, s)


if __name__ == '__main__':
    unittest.main(exit=False)
