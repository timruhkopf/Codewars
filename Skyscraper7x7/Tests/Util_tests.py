from Skyscraper7x7.Solver.Solver import Skyscraper

class Util_tests:
    def tearDown(self) -> None:
        self.assertEqual(Skyscraper(self.clues).solve(), self.solution)

        del self.clues
        del self.solution
