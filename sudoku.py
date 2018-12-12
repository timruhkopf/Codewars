problem = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

solution = [[9, 2, 6, 5, 8, 3, 4, 7, 1],
            [7, 1, 3, 4, 2, 6, 9, 8, 5],
            [8, 4, 5, 9, 7, 1, 3, 6, 2],
            [3, 6, 2, 8, 5, 7, 1, 4, 9],
            [4, 7, 1, 2, 6, 9, 5, 3, 8],
            [5, 9, 8, 3, 1, 4, 7, 2, 6],
            [6, 5, 7, 1, 3, 8, 2, 9, 4],
            [2, 8, 4, 7, 9, 5, 6, 1, 3],
            [1, 3, 9, 6, 4, 2, 8, 5, 7]]


def solve (problem):
    # This solution reduces the paths need to traverse.
    # index on (row , column, block) = (i, j, i//3 + j//3 + (i//3)*2).
    sudokuindex = list((r, c, r // 3 + c // 3 + (r // 3) * 2) for r in range(9) for c in range(9))
    zero = [(r, c, b) for r, c, b in sudokuindex if problem[r][c] == 0]
    # TODO: change the sorting of zero for efficiency gains;
    # e.g. by number of possibilities to make correct decisions early
    # at the cost of little marginal information gain (locally) for each choice
    # consider zerodict = {(r,c,b):candrow[r] & candcol[c] & candblock[b] for r, c, b in sudokuindex if problem[r][c] == 0}

    B = [[], [], [], [], [], [], [], [], []]
    for r, c, b in sudokuindex:
        if problem[r][c] != 0:
            B[b].append(problem[r][c])
    candblock = [set(range(1, 10)) - set(block) for block in B]
    candrow = [set(range(10)) - set(row) for row in problem]
    candcol = [set(range(10)) - set(column) for column in list(zip(*problem))]  # make use of transpose

    def memoize (f):
        def helper (position, counter):
            helper.calls += 1
            helper.memo[position] = f(position, counter)
            return helper.memo[position]

        helper.calls = 0
        helper.memo = {}
        return helper

    @memoize
    def solv (position, counter):  # TODO: counter in decorator
        r, c, b = position
        S = candrow[r] & candcol[c] & candblock[b]
        for s in S:
            if counter + 1 == len(zero):  # base case: last zero value is reached
                return s
            else:  # go further down on path with current s
                candrow[r].difference_update({s})
                candcol[c].difference_update({s})
                candblock[b].difference_update({s})
                sol = solv(zero[counter + 1], counter + 1)

                if bool(sol):  # the next step yielded a non empty solution
                    return s
                else:  # the next zero index returns {}
                    # i.e. it has no applicable choices: Go up
                    # add s to sets it was removed from
                    candrow[r].update({s})
                    candcol[c].update({s})
                    candblock[b].update({s})
                    continue
        return {}

    solv(position=zero[0], counter=0)

    print('it required {} calls to solve the problem'.format(solv.calls))
    # print(solv.memo)

    for (r, c, b), val in solv.memo.items():
        problem[r][c] = val

    return problem


print(solve(problem))

a = sudoku([[0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 5, 8, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0, 8, 5],
            [0, 1, 0, 4, 7, 0, 6, 0, 0],
            [0, 0, 6, 0, 0, 0, 5, 0, 7],
            [5, 0, 7, 0, 3, 9, 0, 4, 0],
            [7, 6, 0, 0, 0, 8, 0, 0, 0],
            [0, 0, 0, 9, 0, 0, 8, 1, 0],
            [0, 0, 9, 0, 0, 0, 0, 0, 0]])