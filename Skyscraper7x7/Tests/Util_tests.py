from Skyscraper7x7.Solver.Solver import Skyscraper

class Util_tests:
    def tearDown(self) -> None:
        self.assertEqual(Skyscraper(self.clues).solve(), self.solution)

        del self.clues
        del self.solution

    # def tearDown(self):
    #     from Skyscraper7x7.Strategies.StrategyStack import StrategyStack
    #     sky = Skyscraper(self.clues)
    #     sky.downtown_row = {r: list(sky.pclues[sky.rowclues[r]]) for r in range(sky.probsize)}
    #     sky.downtown_col = {c: list(sky.pclues[sky.colclues[c]]) for c in range(sky.probsize)}
    #     StrategyStack.execute(sky, row=0)
    #
    #     provided = tuple(tuple(sky.downtown_row[i][0]) for i in range(sky.probsize))
    #
    #     self.assertEqual(self.solution, provided)
