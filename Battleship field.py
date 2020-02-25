import numpy as np


def validate_battlefield(field):
    #https://www.codewars.com/kata/52bb6539a4cf1b12d90005b7/train/python
    field = np.array(field)
    battlesquare = [field[i:i + 2, j:j + 2] for i in range(7) for j in range(7)]

    cyclicfilters = [[[1, 1, 1, 0][i - j] for i in range(4)] for j in range(4)] # cyclic permutation

    filter = [np.array(f).reshape(2, 2) for f in cyclicfilters]

    for i, j in filter:
        if np.sum(x * i) == 3:
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
