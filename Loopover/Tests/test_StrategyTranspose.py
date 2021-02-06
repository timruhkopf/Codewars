import unittest

from Loopover.Board.Cyclic_shift import Cyclic_shift_board
from Loopover.Board.Cyclic_shift_debug import board
from Loopover.Strategies.StrategyTranspose import StrategyTranspose


class Test_StrategyTranspose(unittest.TestCase):

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
            c = Cyclic_shift_board(p)
            c.solved_board = s

            StrategyTranspose.execute_strategy(c)
            self.assertEqual(c.toList(), c.solved_board)  # solution is also transposed

            # ensure that the original board can be solved using the translated
            # 'transposed' solution
            d = Cyclic_shift_board(p)
            d.solved_board = s

            for step in d.solution:
                d.shift(step)

            self.assertEqual(c.toList(), c.solved_board)  # solution is also transposed


if __name__ == '__main__':
    unittest.main(exit=False)
