import re
from operator import mul, add, truediv
from collections import deque, defaultdict

subdeq = deque()
op = defaultdict(lambda: add, {'/': truediv, '*': mul})


def calc(expression):
    expression = expression.replace(' ', '').replace('--', '+').replace('+-', '-')

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

    # figure out (entire) nesting structure of parenthesis
    nested = lambda y, x: x[0] > y[0] and x[1] < y[1]  # x nested in y
    brackets = {k: list(v for v in pairs if nested(k, v)) for k in pairs}
    bracket_order = {k: len(brackets[k]) for k in pairs}  # hierarchy level

    # keep only first inner brackets
    for k in brackets.keys():
        for tup in sorted(brackets[k]):
            for nest in sorted(brackets[k]):
                if nested(tup, nest):
                    brackets[k].remove(nest)

    # replace the lowest hierarchy brackets
    regex = re.compile(r'([\/\*])?([\+\-]?\d*\.\d+|[\+\-]?\d+)')
    regex.findall('-35*-5')
    for sl in [k for k, v in bracket_order.items() if v == 0]:
        brackets[sl] = str(eval_flat_expression(regex.findall(expression[sl[0] + 1:sl[1]])))

    # replace each bracket hierarchy's lower levels
    # reverse ensures, that replacements do not change the indicies!
    for i in sorted(set(bracket_order.values()) - {0}):
        for eins in sorted([k for k, v in bracket_order.items() if v == i], reverse=True):
            expr = expression[eins[0] + 1:eins[1]]

            for nuller in sorted(brackets[eins], reverse=True):
                expr = '{}{}{}'.format(expr[:nuller[0] - eins[0] - 1], brackets[nuller], expr[nuller[1] - eins[0]:])
                brackets.pop(nuller)
                expr = expr.replace(' ', '').replace('--', '+').replace('+-', '-')

            brackets[eins] = str(eval_flat_expression(regex.findall(expr)))

    for br in sorted(brackets.keys(), reverse=True):
        expression = '{}{}{}'.format(expression[:br[0]], brackets[br], expression[br[1] + 1:])

    expression = expression.replace(' ', '').replace('--', '+').replace('+-', '-')
    return eval_flat_expression(regex.findall(expression))


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
    # assert calc('(2+2) + (3-3) * (2 / (2 + 3.33) * 4) - -6 * (3-(3/1))') == 4.0
    assert calc('(-83)/(-60/59*-(20))*(35*-(((-(78+92))))+21)') == -24366.655833333334
    assert calc('(-76)/(-14+98+(19))/(17/-(((-(-84*-65))))-26)') == 0.028382786499353052
    assert calc("3 -(-1)") == 4
    assert calc('(-64) * (94 / -13 / -(3)) - (62 * -((((-45 + 46)))) + -6)') == -86.25641025641025  # carefull *-
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
