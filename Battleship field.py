import numpy as np


def validate_battlefield(field):
    # https://www.codewars.com/kata/52bb6539a4cf1b12d90005b7/train/python
    field = np.array(field)

    # setting up filters for convolution
    cyclicfilters = [np.array([[1, 1, 1, 0][i - j] for i in range(4)]).reshape(2,2) for j in range(4)]
    crossfilters = [np.array([[1, 0], [0, 1]]), np.array([[0, 1], [1, 0]])]

    # convoltion over field snippets
    for i in range(7):
        for j in range(7):
            for v, filter in zip([3, 2], [cyclicfilters, crossfilters]):
                if any(map(lambda f: np.sum(f * field[i:i + 2, j:j + 2]) == v, filter)):
                    return False


if __name__ == '__main__':
    battlefield = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                   [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                   [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
                   [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                   [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                   [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

validate_battlefield(battlefield) == True
