import unittest

from delta_generators import delta


class Test_delta(unittest.TestCase):

    def test_generator_1stdiff(self):
        # test for a generator
        gen = delta(values=(x ** 2 for x in range(30)), n=1)
        self.assertEqual([next(gen) for i in range(10)], [1, 3, 5, 7, 9, 11, 13, 15, 17, 19])

    def test_generator_2nddiff(self):
        gen = delta(values=(x ** 2 for x in range(30)), n=2)
        self.assertEqual([next(gen) for i in range(10)], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2])

    def test_list(self):
        gen = delta(values=list(x ** 2 for x in range(30)), n=3)
        self.assertEqual([next(gen) for i in range(10)], [0] * 10)

    def test_stopiteration(self):
        # notice, how higher differences must raise earlier (since there are fewer
        # elements at each subsequent level)
        gen = delta(values=(x ** 2 for x in range(10)), n=2)
        self.assertEqual(list(gen), [2] * 8)  # < -------

    # official tests -----------------------------------------------------------
    def test_simple_finite(self):
        self.assertEqual(list(delta([1, 2, 3, 4, 5, 6], 1)), [1, 1, 1, 1, 1])
        self.assertEqual(list(delta([3, 3, -5, 77], 2)), [-8, 90])
        self.assertEqual(list(delta([1.5] * 10, 9)), [0.0])
        self.assertEqual(list(delta([1, -1, 1, -1], 3)), [-8])

    def test_simple_infinite(self):
        first_n = lambda g, n: [next(g) for _ in range(n)]

        def ones():
            while True:
                yield 1

        self.assertEqual(first_n(delta(ones(), 1), 1000), [0] * 1000)
        self.assertEqual(first_n(delta(ones(), 100), 1000), [0] * 1000)

        def up():
            a, b = 0, 1
            while True:
                yield a
                a, b = a + b, b + 3

        self.assertEqual(first_n(delta(up(), 1), 10), [1, 4, 7, 10, 13, 16, 19, 22, 25, 28])
        self.assertEqual(first_n(delta(up(), 2), 10), [3] * 10)

    def test_other_types(self):
        class Potion:
            def __init__(self, name):
                self.name = name

            def __sub__(self, other):
                return Potion(other.name + self.name)

        vals = [set([6, 2, 'A']), set([2, 'B', 8]), set(['A', 'B'])]
        self.assertEqual(list(delta(vals, 1)), [{8, 'B'}, {'A'}])
        self.assertEqual(list(delta(vals, 2)), [{'A'}])

        vals = [Potion("ko"), Potion("sham"), Potion("ro"), Potion("da")]
        self.assertEqual([v.name for v in delta(vals, 1)], ["kosham", "shamro", "roda"])
        self.assertEqual([v.name for v in delta(vals, 2)], ["koshamshamro", "shamroroda"])

    # (single failing test) ---------------------------------------------------
    def test_stopiteration_fail(self):
        vals = [-1661, -1303, 860, -1076, 1866, 1740, 297, -634, 1254, -1892, 121, 42, -1316, -1028, -211, -559, -677,
                1576, 1552, -827, -564, 1782, 1857, -1048, -118, -160, -54, -798, -786, -110, 659, 1945, 481, -1304,
                -267, 1757, 1126, 609, 1207, 365, 563, -1767, 740, -295, -504, -889, -908, 1802, 660, 1929, 272, -487,
                -724, 753, 330, 5, -1192, 1071, -1773, -403, -1965, -655, -1538, 1780, 775, 1394, -1119, -1212, 1060,
                -11, -1807, -1955, -200, 150, -1465, -727, 1021, 1558, 872, -346, -1252, 1278, 1941, -344, 1781, 1803,
                -115, 1778, -819, -140, -663, -1690, -278, 1532, 1145, 1560, -705, 870, 1732, -613, 763, 1998, 1408,
                -424, -1751, -415, 1411, -1502, -155, -787, -442, -1463, -771, -389, -1621, -366, -1815, 607, 1313, 747,
                -1056, 963, 758, -31, -512, -1429, 1610, 941, 232, -584, -1654, -534, 971, -1521, 437, 588, 874, -1435,
                -388, -1960, 1354, -1907, -1651, 1859, 71, 601, 126, -1552, -1608, 1794, -1033, 431, 1837, 1109, -1792,
                132, -1747, -796, 672, -1432, -1410, 1743, 1919, -618, -592, -258, 223, 1581, 301, 1183, 1672, -70,
                1713, -686, 684, 1007, 619, 1729, -350, 1507, 263, 544, -1447, 519, -170, -366, -1141, 207, 1831, 1012,
                1800, 103, -466, -138, 581, 679, -678, 1084, -1354, -1443, -984, -1789, 309, 1853, -840, -820, -1306,
                1327, -1197, -1746, 451, -1491, 852, -1467, -1704, 1615, -1561, -1406, -172, 1204, -1511, 816, 260,
                -1228, 816, 1219, -182, 978, 861, -1573, 246, 1106, -43, -1185, -72, -1253, 1689, 912, 583, 216, 1950,
                133, -1376, -1493, 677, 1456, 1682, 1975, 252, -661, 1463, 1458, -694, -1115, -1454, 26, 1749, 63, 259,
                -1889, 112, 1674, 780, -55, -834, 1803, -971, 1635, 731, 734, -1289, -440, -1748, 663, -585, 679, -62,
                -1789, -1315, -1303, -1829, 1494, -1556]

        list(delta(vals, 283))  # this must not raise !!!!!!!!!!!!


if __name__ == '__main__':
    unittest.main(exit=False)
