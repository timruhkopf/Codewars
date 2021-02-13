def board(strboard):
    return [[v for v in row] for row in strboard.strip().replace(' ', '').split('\n')]
