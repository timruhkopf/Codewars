from Sudoku.Board.MultiSudoku import Sudoku


def sudoku_solver(puzzle):
    """kata's required interface"""
    return Sudoku(problem=puzzle).solve()
