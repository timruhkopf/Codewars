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

# (EVEN SHORTER VERSION OF IT) -------------------------------------------------
# import re
#
# def simplify(poly):
#     return M().simplify(poly)
#
# class M:
#     regex = re.compile(r'([+\-]?)(\d*)([a-z]+)')
#     default = ('+', '1', '_')
#
#     def simplify(self, poly):
#         terms = self.regex.findall(poly)
#         terms = [[self.default[i] if val == '' else val for i, val in enumerate(tup)] for tup in terms]
#
#         abbrev = {''.join(sorted(k)): sum([int(''.join([sign, val])) for sign, val, lit in terms if lit == k])
#                   for k in set(t[2] for t in terms)}
#         abbrev = {k:v for k, v in abbrev.items() if v != 0}
#
#         terms = sorted([(v, k) for k, v in abbrev.items()],  key=lambda tup: (len(tup[1]) , tup[1]))
#         return ''.join([''.join([['', '+'][val >= 0], ['', str(val)][abs(val)!=1], k]) for val, k in terms]).lstrip('+')  # FIXME: this line fails!
#
#




if __name__ == '__main__':
    # ("Test reduction by equivalence")

    M().simplify("-a+5ab+3a-c-2a")
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
