import unittest
from Loopover.StrategyToprow import StrategyToprow
from Loopover.StrategyLiftshift import StrategyLiftshift
from Loopover.Cyclic_shift import Cyclic_shift_board
# TODO: as input to the test_cases


class TestStrategies(unittest.TestCase):
    def test_Liftshift(self):
        # Cyclic_shift_board
        pass

    def test_find_sort_graphs(self):
        #  # (find_sort_graphs) -------------------------------------------------------
        #     target_row = ['A', 'B', 'C', 'D', 'E']
        #     row = ['B', 'C', 'D', 'E', 'A']  # single shift right suffices
        #
        #     row = ['B', 'E', 'A', 'C', 'D']
        pass

    def test_split_subgraphs(self):
        #     # single graph
        #     assert StrategyToprow.split_subgraphs({'A': 'C', 'B': 'D', 'C': 'B', 'D': 'E', 'E': 'A'}) == \
        #            [{'A': 'C', 'B': 'D', 'C': 'B', 'D': 'E', 'E': 'A'}]
        #
        #     # two closed subgraphs
        #     assert StrategyToprow.split_subgraphs({'A': 'D', 'C': 'E', 'D': 'A', 'E': 'C'}) in \
        #            ([{'A': 'D', 'D': 'A', }, {'C': 'E', 'E': 'C'}],
        #             [{'C': 'E', 'E': 'C'}, {'A': 'D', 'D': 'A', }])
        pass

    def test_choose_strategy(self):
        pass

    def test_toprow_example(self):
        # # # @test.it('Test 4x5')
        # run_test('ACDBE\nFGHIJ\nKLMNO\nPQRST',
        #          'ABCDE\nFGHIJ\nKLMNO\nPQRST', False)
        #
        # # @test.it('Test 5x5 (1)')
        # run_test('ACDBE\nFGHIJ\nKLMNO\nPQRST\nUVWXY',
        #          'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', False)

        # initalise board then immediately call Strategy.toprow

        pass

if __name__ == '__main__':
    unittest.main()
