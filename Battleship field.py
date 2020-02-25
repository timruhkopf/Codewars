import numpy as np


def validate_battlefield(field):
    """https://www.codewars.com/kata/52bb6539a4cf1b12d90005b7/train/python"""
    field = np.array(field)

    # early kill if to many ones
    ones = np.sum(field)
    if ones != 20:
        return False

    # setting up filters for convolution
    cyclicfilters = [np.array([[1, 1, 1, 0][i - j] for i in range(4)]).reshape(2, 2) for j in range(4)]
    crossfilters = [np.array([[1, 0], [0, 1]]), np.array([[0, 1], [1, 0]])]

    # convoltion over field snippets (allows early stopping)
    for i in range(9):
        for j in range(9):
            for v, filter in zip([3, 2], [cyclicfilters, crossfilters]):
                if any(map(lambda f: np.sum(f * field[i:i + 2, j:j + 2]) == v, filter)):
                    return False

    shipcounter = {k: 0 for k in [4, 3, 2]}
    for ind, ship in zip([7, 8, 9], [4, 3, 2]):
        for j in range(10):
            for i in range(ind):  #
                if sum(field[j, i:i + ship]) == ship:
                    shipcounter[ship] += 1
                if sum(field[i:i + ship, j]) == ship:
                    shipcounter[ship] += 1

    shipcounter[1] = np.sum(field)
    if shipcounter == {4: 1, 3: 2, 2: 3, 1: 4}:
        return True
    else:
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
