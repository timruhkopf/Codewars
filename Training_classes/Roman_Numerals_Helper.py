class RomanNumerals:
    """https://www.codewars.com/kata/51b66044bce5799a7f000003"""

    _symbol = ['', 'I', 'V', 'X', 'L', 'C', 'D', 'M']
    _value = [0, 1, 5, 10, 50, 100, 500, 1000]
    translator_roman = {s: v for s, v in zip(_symbol, _value)}
    translator_int = {v: s for s, v in zip(_symbol, _value)}

    @classmethod
    def to_roman(cls, integer: int):
        temp = []
        rev_value = list(reversed([int(s) for s in str(integer)]))
        for power, high in enumerate(rev_value):
            if high in (4, 9):
                # first and second letters for value 4 or 9 by difference to next higher letter
                temp.append(cls.translator_int[10 ** power] + cls.translator_int[(high + 1) * 10 ** power])
            elif high == 5:
                # e.g. 300: CCC
                temp.append(cls.translator_int[high * 10 ** power])

            else:
                # below or above 5 but not 4, 9 e.g. DC 600
                # THIS REQUIRES  translator_int {0:''}
                temp.append(
                    cls.translator_int[(high // 5) * 5 * 10 ** power] + cls.translator_int[10 ** power] * (high % 5))

        return ''.join(reversed(temp))

    @classmethod
    def from_roman(cls, string: str):
        # corner case single character
        if len(string) == 1:
            return cls.translator_roman[string]

        # check if smaller number before larger
        value_list = [cls.translator_roman[s] for s in string]
        number = 0
        iterator = zip(value_list, value_list[1:])
        while True:
            try:
                prev, nxt = next(iterator)
                if prev < nxt:
                    number += nxt - prev
                    next(iterator)
                else:
                    number += prev
            except StopIteration:
                break

        # after stopiteration: what to do with last value?
        if prev < nxt:
            return number
        else:
            return number + nxt
