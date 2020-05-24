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
    brackets = {k: list(v for v in pairs if nested(k, v)) for k in pairs}
    bracket_order = {k: len(brackets[k]) for k in pairs}

    # keep only first inner brackets
    for k in brackets.keys():
        for tup in sorted(brackets[k]):
            for nest in sorted(brackets[k]):
                if nested(tup, nest):
                    brackets[k].remove(nest)

    # start with 0 len and evaluate.
    regex = re.compile(r'([\/\*])?([\-]?\d*\.\d+|[\-]?\d+)')
    for sl in [k for k, v in bracket_order.items() if v == 0]:
        brackets[sl] = str(eval_flat_expression(regex.findall(expression[sl[0] + 1:sl[1]])))

    # reverse ensures, that replacements do not change the indicies!
    for eins in sorted([k for k, v in bracket_order.items() if v == 1], reverse=True):
        expr = expression[eins[0]+1:eins[1]]
        for nuller in sorted(brackets[eins], reverse=True):
            expr = '{}{}{}'.format(expr[:nuller[0]-eins[0]-1], brackets[nuller],  expr[nuller[1]-eins[1]+1:])

        brackets[eins] = str(eval_flat_expression(regex.findall(expr)))

    print()

    # re.split('\+|\-|\*|\/', '1.2+2-3/6*4')  # separating numbers by operator delimiter
    # re.findall('[+\-\*\/]+', '1.2+2-3/-6*4')  # find all operations (including '/-')

    for sl in sorted(brackets, key=lambda k: len(brackets[k])):
        if len(brackets[sl]) == 0:
            str(eval_flat_expression(regex.findall(expression[sl[0] + 1:sl[1]])))



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

    calc('(2+2) + (3-3) * (2 / (2 + 3.33) * 4) - -6 * (3-(3/1))')
    calc('(-64) * (94 / -13 / -(3)) - (62 * -((((-45 + 46)))) + -6)')  # carefull *-
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
