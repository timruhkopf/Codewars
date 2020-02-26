import numpy as np


def solve_puzzle(clues):
    clues = [[clues[i+j*7] for i in range(7)] for j in  range(4)] # columclues must be [::-1]
    # rowclues =
    # columnclues
    solution = np.zeros((7, 7))

    solution


if __name__ == '__main__':
    from Test_Codewars import test

    test.describe("7x7")
    test.it("medium")
    test.assert_equals(
        solve_puzzle([7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4]),
        [[1, 5, 6, 7, 4, 3, 2],
         [2, 7, 4, 5, 3, 1, 6],
         [3, 4, 5, 6, 7, 2, 1],
         [4, 6, 3, 1, 2, 7, 5],
         [5, 3, 1, 2, 6, 4, 7],
         [6, 2, 7, 3, 1, 5, 4],
         [7, 1, 2, 4, 5, 6, 3]]
    )
    test.it("very hard")
    test.assert_equals(
        solve_puzzle([0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1]),
        # for a _very_ hard puzzle, replace the last 7 values with zeroes
        [[7, 6, 2, 1, 5, 4, 3],
         [1, 3, 5, 4, 2, 7, 6],
         [6, 5, 4, 7, 3, 2, 1],
         [5, 1, 7, 6, 4, 3, 2],
         [4, 2, 1, 3, 7, 6, 5],
         [3, 7, 6, 2, 1, 5, 4],
         [2, 4, 3, 5, 6, 1, 7]]
    )
