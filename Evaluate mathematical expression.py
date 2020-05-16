def calc(expression):
    left = [i for i, _ in enumerate(expression) if _ == '(']
    right = [i for i, _ in enumerate(expression) if _ == ')']

    # find pairs of sorted brackets
    pairs = []
    for i in reversed(left):
        for j in right:
            if j > i:
                pairs.append((i, j))
                left.remove(i)
                right.remove(j)






if __name__ == '__main__':
    # calc('-7 * -(6 / 3)') == 14
    calc('(2 / (2 + 3.33) * 4) - -6*(2+(3-1))') == 7.50093808630394



