def memorize(f):
    def helper(x):
        memo = [x]
        while f(memo[-1]) not in memo or x % 13 != f(memo[-1]) % 13:
            memo.append(f(memo[-1]))
        return memo[-1]
    return helper


@memorize
def thirt(n):
    n = str(n)
    return sum([int(i) * j for i, j in zip(reversed(n), [1, 10, 9, 12, 3, 4]*(len(n)//5 + (len(n) % 5 > 0)))])



if __name__ == '__main__':
    assert (thirt(1234567) == 87)
    assert (thirt(8529) == 79)
    assert (thirt(85299258) == 31)
    assert (thirt(5634) == 57)
    assert (thirt(1111111111) == 71)
    assert (thirt(987654321) == 30)