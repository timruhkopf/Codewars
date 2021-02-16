from Skyscraper7x7.helper_Interpretation import timeit, _interpret_clues, mem_visability


# TODO keep the functinonal style in seperate file - as alternative solution
#  and point of reference

# TODO Refactor into class with multiple strategies. lazyily compute class attribute: permutations (only when needed
#  and return the correct size from the infered shape.


@timeit
@mem_visability(probsize=7)  # TODO INFER PROBLEMSIZES, rather than hard setting them for the kata
def solve_puzzle(clues, probsize, pclues):
    """
    4*4 Skyscraper: https://www.codewars.com/kata/5671d975d81d6c1c87000022
    6*6 Skyscraper: https://www.codewars.com/kata/5679d5a3f2272011d700000d
    7*7 Skyscraper: https://www.codewars.com/kata/5917a2205ffc30ec3a0000a8
    """
    colclues, rowclues = _interpret_clues(clues, probsize)

    downtown_row = {r: list(pclues[rowclues[r]]) for r in range(probsize)}
    downtown_col = {c: list(pclues[colclues[c]]) for c in range(probsize)}

    def update(col, margin=1):
        """column update for margin== 1, rowupdate if margin == 0"""

        pos1 = (downtown_row, downtown_col)[margin]
        pos2 = (downtown_row, downtown_col)[margin - 1]

        # updating rows indepenendly based on column
        fix = [set(column) for column in zip(*pos1[col])]
        for i, valid in enumerate(fix):
            pos2[i] = [tup for tup in pos2[i] if tup[col] in valid]

        _update_det(pos1, fix, col)

    def _update_det(pos1, fix, col):
        """update deterministics across "columns" & early stopping!"""
        uniques = list((i, v) for i, v in enumerate(fix) if len(v) == 1)
        stack = {k: [] for k in range(probsize)}
        for j in {*range(probsize)} - {col}:
            for tup in pos1[j]:
                for i, v in uniques:
                    if tup[i] in v:
                        pos1[j].remove(tup)
                        stack[j].append(tup)
                        break
        return stack  # relevant only for last 7*7er case

    def update_2ndstage(row):
        """recursive solving for the last remaining ambiguous case"""
        for choice in downtown_row[row]:
            stack = _update_det(pos1=downtown_row, fix=[set([v]) for v in choice], col=row)
            downtown_row[row] = [choice]

            after = [len(row) for row in downtown_row.values()]
            if not all(after):
                _revert(stack)
                continue

            elif row != probsize - 1:  # there are more rows
                if update_2ndstage(row + 1):
                    return True
                else:
                    continue

            elif after == [1, 1, 1, 1, 1, 1, 1]:
                return True

        if after != [1, 1, 1, 1, 1, 1, 1]:  # all choices faulty
            _revert(stack)
            return False

    def _revert(stack):
        for k, v in stack.items():
            downtown_row[k].extend(v)

    # (1st stage updating) solves all unambigous cases -------------------------
    before = []
    after = [len(a[i]) for a in (downtown_row, downtown_col) for i in range(probsize)]
    while before != after:
        before = after
        for row in sorted(range(probsize), key=lambda i: len(downtown_row[i])):
            update(row, margin=0)

        for col in sorted(range(probsize), key=lambda i: len(downtown_col[i])):
            update(col, margin=1)

        after = [len(a[i]) for a in (downtown_row, downtown_col) for i in range(probsize)]

    # (2nd stage updating) solves ambigous cases -----------------------
    if after != [1, 1, 1, 1, 1, 1, 1]:
        update_2ndstage(row=0)

    if probsize == 7:
        return [list(downtown_row[i][0]) for i in range(probsize)]
    return tuple(tuple(downtown_row[i][0]) for i in range(probsize))
