problem = [[9, 0, 0, 0, 8, 0, 0, 0, 1],
           [0, 0, 0, 4, 0, 6, 0, 0, 0],
           [0, 0, 5, 0, 7, 0, 3, 0, 0],
           [0, 6, 0, 0, 0, 0, 0, 4, 0],
           [4, 0, 1, 0, 6, 0, 5, 0, 8],
           [0, 9, 0, 0, 0, 0, 0, 2, 0],
           [0, 0, 7, 0, 3, 0, 2, 0, 0],
           [0, 0, 0, 7, 0, 5, 0, 0, 0],
           [1, 0, 0, 0, 4, 0, 0, 0, 7]]

solution = [[9, 2, 6, 5, 8, 3, 4, 7, 1],
            [7, 1, 3, 4, 2, 6, 9, 8, 5],
            [8, 4, 5, 9, 7, 1, 3, 6, 2],
            [3, 6, 2, 8, 5, 7, 1, 4, 9],
            [4, 7, 1, 2, 6, 9, 5, 3, 8],
            [5, 9, 8, 3, 1, 4, 7, 2, 6],
            [6, 5, 7, 1, 3, 8, 2, 9, 4],
            [2, 8, 4, 7, 9, 5, 6, 1, 3],
            [1, 3, 9, 6, 4, 2, 8, 5, 7]]

# This solution reduces the paths need to traverse.
# (1) finding the sets of applicable values in each dimension (row, column, block)
candrow = [set(range(10)) - set(row) for row in problem]
candcol = [set(range(10)) - set(column) for column in list(zip(*problem))]  # make use of transpose

# index on (row , column, block) = (i, j, i//3 + j//3 + (i//3)*2). # traverses rowwise in problem
sudokuindex = list((r, c, r // 3 + c // 3 + (r // 3) * 2) for r in range(9) for c in range(9))
zero = [(r,c,b) for r, c, b in sudokuindex if problem[r][c] == 0]

B = [[], [], [], [], [], [], [], [], []]
for r, c, b in sudokuindex:
    if problem[r][c] != 0:
        B[b].append(problem[r][c])
candblock = [set(range(1,10)) - set(block) for block in B]


def memoize (f):
    memo = {}

    def helper (position, counter):
        '''keep track on memo & current index position & call counter'''
        helper.calls += 1
        memo[position] = f(position, counter) # overrides the index position or create it if hasn't been there
        return memo

    helper.calls = 0
    return helper

@memoize
def solv(position, counter):
    r,c,b = position
    S = candrow[r] & candcol[c] & candblock[b]
    for s in S:
        if counter +1 == len(zero): # & len(S) == 1: not necessary, but explicit
            # base case; the last zero value is reached and has only one solution
            return s
        else:
            # we have a candidate s
            # remove from se return {}ts
            candrow[r].difference_update({s})
            candcol[c].difference_update({s})
            candblock[b].difference_update({s})
            sol = solv(zero[counter + 1], counter+1) # solv.current+1

            if bool(sol): # the next step yielded a non empty solutions
                return s
            else:  # the next zero index returns {} i.e. it has no applicable choices
                # add s to sets it was removed from
                candrow[r].update({s})
                candcol[c].update({s})
                candblock[b].update({s})
                continue # just for visual purposes.
    return {}

solv(position = zero[0], counter = 0)

print(solv.calls)
print(solv.current)

# hello github
#         if bool(solut):
#             helper.current += 1
#
#         else: # || bool(memo[position])
#             helper.current -= 1
#
#         helper.current = 0

