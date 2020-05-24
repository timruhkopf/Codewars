import re


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

    # figure out nesting structure of parenthesis
    nested = lambda y, x: x[0] > y[0] and x[1] < y[1]  # x nested in y
    brackets = {k: [v for v in pairs if nested(k, v)] for k in pairs}

    # execution order by length of brackets !
    regex = re.compile(r'([+\-/*]?)(\d*)')
    for sl in sorted(brackets, key=lambda k: len(brackets[k])):
        if len(brackets[sl]) == 0:
            regex.findall(expression[sl[0]:sl[1]])

        # at execution pull the slice and replace the nested brackets by their literal value
        # carefull to replace starting from behind to not mess up the indicies

        # regex over flattened sub expression

        # search for devision & multiplication

        # do addition

    print()




if __name__ == '__main__':
    calc('(2+2) + (3-3) * (2 / (2 + 3.33) * 4) - -6 * (3-(3/1))')
    calc('-7 * -(6 / 3)') == 14
    calc('(2 / (2 + 3.33) * 4) - -6') == 7.50093808630394
    calc('(2+2) + (3-3)')
    # calc('-7 * -(6 / 3)') == 14
    calc('(2 / (2 + 3.33) * 4) - -6*(2+(3-1))') == 7.50093808630394
    '(2/ a * 4) -- 6*(b)'

    calc('-(-(-(-1)))')
    calc('(((((-1)))))')
    calc('13 * 36 / 5 / -76 * 71 - 70 * -21 - -80')  # carefull --

    calc('(-64) * (94 / -13 / -(3)) - (62 * -((((-45 + 46)))) + -6)')  # carefull *-
    calc('-(22) * (-14 / 32 + (52)) - (-12 + (((-(23 / 74)))) + 50)')

