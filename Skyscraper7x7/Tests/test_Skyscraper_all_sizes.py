import unittest

from ..Solver.Solver import Skyscraper


class TestSkyscraper(unittest.TestCase):
    # def test_speedincrease(self):
    #     """This test is aimed at pclues caching and loading it after the first time"""
    #     sky = Skyscraper([2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2])
    #     # TODO time solving
    #     solution = sky.solve()
    #     self.assertEqual(solution,
    #                      ((3, 4, 2, 1),
    #                       (1, 2, 3, 4),
    #                       (2, 1, 4, 3),
    #                       (4, 3, 1, 2)))
    #
    #     sky = Skyscraper([2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2])
    #     # TODO time solving
    #     sky.solve()
    #
    #     # self.assertTrue(first_time > second_time)

    def test_continously(self):
        sky = Skyscraper([2, 1, 3, 2, 3, 1, 2, 3, 3, 2, 2, 1, 1, 2, 4, 2])
        self.assertEqual(sky.solve(),
                         ((3, 4, 2, 1),
                          (1, 2, 3, 4),
                          (2, 1, 4, 3),
                          (4, 3, 1, 2)))

        self.assertIsNotNone(sky._pclues[4])

        sky = Skyscraper((0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0))
        self.assertEqual(sky.solve(),
                         ((5, 6, 1, 4, 3, 2),
                          (4, 1, 3, 2, 6, 5),
                          (2, 3, 6, 1, 5, 4),
                          (6, 5, 4, 3, 2, 1),
                          (1, 2, 5, 6, 4, 3),
                          (3, 4, 2, 5, 1, 6)))

        sky = Skyscraper([3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3])
        self.assertEqual(sky.solve(),
                         [[2, 1, 4, 7, 6, 5, 3],
                          [6, 4, 7, 3, 5, 1, 2],
                          [1, 2, 3, 6, 4, 7, 5],
                          [5, 7, 6, 2, 3, 4, 1],
                          [4, 3, 5, 1, 2, 6, 7],
                          [7, 6, 2, 5, 1, 3, 4],
                          [3, 5, 1, 4, 7, 2, 6]])

        self.assertIsNotNone(sky._pclues[4])
        self.assertIsNotNone(sky._pclues[6])
        self.assertIsNotNone(sky._pclues[7])


if __name__ == '__main__':
    unittest.main()
