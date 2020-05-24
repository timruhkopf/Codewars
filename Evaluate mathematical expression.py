import re
from operator import mul, add, truediv
from collections import deque, defaultdict

subdeq = deque()
op = defaultdict(lambda: add, {'/': truediv, '*': mul})


def calc(expression):
    expression = expression.replace(' ', '').replace('--', '-').replace('+-', '-')

    # find pairs of sorted brackets
    left = [i for i, _ in enumerate(expression) if _ == '(']
    right = [i for i, _ in enumerate(expression) if _ == ')']
    pairs = []
    for i in reversed(left):
        for j in right:
            if j > i:
                pairs.append((i, j))
                left.remove(i)
                right.remove(j)
                break

    # # validate braket pairs:
    # for tup in pairs:
    #     print(expression[tup[0] + 1:tup[1]])

    # figure out nesting structure of parenthesis
    nested = lambda y, x: x[0] > y[0] and x[1] < y[1]  # x nested in y
    brackets = {k: set(v for v in pairs if nested(k, v)) for k in pairs}
    bracket_order = {k: len(brackets[k]) for k in pairs}

    # # filter brackets such, that only the directly next nested level is avail.
    # for k in [k for k in brackets.keys() if bracket_order[k]!= 0]:
    #     brackets[k].difference_update(set.union(*(brackets[key] for key in brackets[k] if bracket_order[key]!= 0)))
    #
    # for k in brackets.keys():
    #     for tupy in brackets[k]:
    #         for tupx in brackets[k]:
    #             if nested(tupy,tupx):
    #                 brackets[k].remove(tupx)

    # start with 0 len and evaluate.

    # continue with level one and replace

    # execution order by length of brackets !
    regex = re.compile(r'([\/\*])?([\-]?\d*\.\d+|[\-]?\d+)')  # almost correct

    # re.split('\+|\-|\*|\/', '1.2+2-3/6*4')  # separating numbers by operator delimiter
    # re.findall('[+\-\*\/]+', '1.2+2-3/-6*4')  # find all operations (including '/-')

    for sl in sorted(brackets, key=lambda k: len(brackets[k])):
        if len(brackets[sl]) == 0:
            str(eval_flat_expression(regex.findall(expression[sl[0] + 1:sl[1]])))




    print()


def eval_flat_expression(expression):
    global subdeq
    global op

    for operator, val in expression:
        if operator not in ['*', '/']:
            subdeq.append((operator, float(val)))
        else:
            prev = subdeq.pop()
            subdeq.append(('', op[operator](prev[1], float(val))))

    bracket_content = sum(val for _, val in subdeq)
    subdeq.clear()
    return bracket_content


if __name__ == '__main__':
    calc('(-64) * (94 / -13 / -(3)) - (62 * -((((-45 + 46)))) + -6)')  # carefull *-
    calc('(2+2) + (3-3) * (2 / (2 + 3.33) * 4) - -6 * (3-(3/1))')
    calc('13 * 36 / 5 / -76 * 71 - 70 * -21 - -80')
    calc('-7 * -(6 / 3)') == 14
    calc('(2 / (2 + 3.33) * 4) - -6') == 7.50093808630394
    calc('(2+2) + (3-3)')
    # calc('-7 * -(6 / 3)') == 14
    calc('(2 / (2 + 3.33) * 4) - -6*(2+(3-1))') == 7.50093808630394
    '(2/ a * 4) -- 6*(b)'

    calc('-(-(-(-1)))')
    calc('(((((-1)))))')


    calc('-(22) * (-14 / 32 + (52)) - (-12 + (((-(23 / 74)))) + 50)')
