import numpy as np
from itertools import permutations

def validate_battlefield(field):
    #https://www.codewars.com/kata/52bb6539a4cf1b12d90005b7/train/python
    field = np.array(field)
    battlesquare = [field[i:i + 2, j:j + 2] for i in range(7) for j in range(7)]

    per = (set(permutations([1, 1, 1, 0])))
    filter = [np.array(i).reshape(2, 2) for i in per]

    for i,j in filter:
        if np.sum(x * i) == 3:
            return False





