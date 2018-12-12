import itertools

clues = (( 2, 2, 1, 3,  2, 2, 3, 1,  1, 2, 2, 3,  3, 2, 1, 3 ),
         ( 0, 0, 1, 2,  0, 2, 0, 0,  0, 3, 0, 0,  0, 1, 0, 0 ))

outcomes = (
( ( 1, 3, 4, 2 ),
  ( 4, 2, 1, 3 ),
  ( 3, 4, 2, 1 ),
  ( 2, 1, 3, 4 ) ),
( ( 2, 1, 4, 3 ),
  ( 3, 4, 1, 2 ),
  ( 4, 2, 3, 1 ),
  ( 1, 3, 2, 4 ) )
)


# generate information set dictonary:
{key: {} for key in range(5)}

zerocase = list(itertools.permutations([1, 2, 3, 4]))


# positions of informationsets:
# where each number is the index of clue.
# (0,11),(1,10), (2,9), (3,8) # columnwise
# (4,15),(5,14),(6,13),(7,12) # rowwise

# gegeben clueindecies -> info of clue, consider the info sets (0,1,2,3,4)
# that is the clue given and the tupels resulting from that info
# bei column ist das zweite infoset reversed, bei row das erste: da man von oben nach unten und von links nach rechts liest.
# column: {tupels of first condition & reversed tupels of second conditon}
# row : vice versa.

# now pixel-wise look at the values of the sets with row & columns!
# depending on the amount of info in those sets, replace those values that are certain and update the row & column sets
# again look at those that are certain.


import itertools

A = list(itertools.permutations([1, 2, 3, 4]))


def vis (elem):
    visable = 1
    mem = elem[0]
    for a in elem:
        if mem < a:
            mem = a
            visable += 1
        else:
            continue
    return visable


{k: v for k, v in zip(map(vis, A), A)}

clue1 = (2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 2, 3, 3, 2, 1, 3)
solution1 = ((1, 3, 4, 2), (4, 2, 1, 3), (3, 4, 2, 1), (2, 1, 3, 4))

clue2 = (0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0)
solution2 = ((2, 1, 4, 3), (3, 4, 1, 2), (4, 2, 3, 1), (1, 3, 2, 4))
