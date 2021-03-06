import re


def simplify(poly):
    return Multilinear_polynomials(poly).simplify()


class Term(str):
    regex1 = re.compile('([+-])?(\d+?)?([a-z]+)?')  # identify term components

    def __init__(self, p):
        res = list(self.regex1.match(p).groups())

        # Establish defaults for missing arguments
        if res[0] is None:
            res[0] = '+'
        if res[1] is None:
            res[1] = '1'
        if res[2] is None:
            res[2] = '_'

        self.sign = res[0]
        self.val = int(''.join(res[0:2]))
        self.literal = ''.join(sorted(res[2]))

    def __str__(self):
        return ''.join([self.sign, [str(abs(self.val)), ''][abs(self.val) == 1], self.literal])

    def __gt__(self, other):
        return self.literal > other.literal


class Multilinear_polynomials:
    regex0 = re.compile('([+-]?\d?[a-z]+)')  # split up terms

    def __init__(self, poly: str):
        self.terms = [Term(s) for s in self.regex0.findall(poly) if bool(s)]

    def simplify(self):
        abbrev = {k: sum([t.val for t in self.terms if t.literal == k])
                  for k in set(t.literal for t in self.terms)}

        self.terms = sorted([Term(''.join([str(val), k])) for k, val in abbrev.items()],
                            key=lambda t: (len(t.literal), t.literal))
        string = ''.join([str(term) for term in self.terms if '0' not in term])  # carefull with '+'
        return string.lstrip('+')





if __name__ == '__main__':
    # ("Test reduction by equivalence")
    assert (simplify("-a+5ab+3a-c-2a") == "-c+5ab")

    assert (simplify("dc+dcba") == "cd+abcd")

    assert (simplify("2xy-yx") == "xy")

    # ("Test monomial length ordering")
    assert (simplify("-abc+3a+2ac") == "3a+2ac-abc")

    assert (simplify("xyz-xz") == "-xz+xyz")

    # ("Test lexicographic ordering")
    assert (simplify("a+ca-ab") == "a-ab+ac")

    assert (simplify("xzy+zby") == "byz+xyz")

    # ("Test no leading +")
    assert (simplify("-y+x") == "x-y")

    assert (simplify("y-x") == "-x+y")
