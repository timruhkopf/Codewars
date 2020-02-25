import numpy as np
from itertools import permutations

def validate_battlefield(field):
    #https://www.codewars.com/kata/52bb6539a4cf1b12d90005b7/train/python

    per = (set(permutations([1, 1, 1, 0])))
    filter = [np.array(i).reshape(2, 2) for i in per]

    for i,j in filter:
        if np.sum(x * i) == 3:
            return False





