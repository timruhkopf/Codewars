def max_multiple(divisor, bound):
    return [n for n in sorted(range(bound+1), reverse=True) if n % divisor == 0][0]


if __name__ == '__main__':
    assert (max_multiple(2, 7) == 6)
    assert (max_multiple(3, 10) == 9)
    assert (max_multiple(7, 17) == 14)
    assert (max_multiple(10, 50) == 50)
    assert (max_multiple(37, 200) == 185)
    assert (max_multiple(7, 100) == 98)