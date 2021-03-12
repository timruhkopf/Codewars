class RomanNumerals:
    _symbol = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
    _value = [1, 5, 10, 50, 100, 500, 1000]
    translator_sv = {s: v for s, v in zip(_symbol, _value)}
    translator_vs = {v: s for s, v in zip(_symbol, _value)}

    @classmethod
    def to_roman(cls, integer):
        if isinstance(integer, int):
            roman_num = ''
            split_num = [i + '0' * j for i, j in zip(str(integer), sorted(range(len(str(integer))), reverse=True))]
            for n in split_num:
                if int(n) >= 1000:
                    roman_num += cls.translator_vs[1000] * (int(n) // 1000)
                else:
                    roman_num += cls.combine(cls, n)
            return roman_num
        else:
            raise Exception('check your input! give me an integer')

    @classmethod
    def from_roman(cls, string):
        if isinstance(string, str):
            value_list = [cls.translator_sv[i] for i in string]
            if value_list == sorted(value_list, reverse=True):
                return sum(value_list)
            else:
                number = []
                for i in range(len(value_list) - 1):
                    if value_list[i] < value_list[i + 1]:
                        number.append(value_list[i + 1] - value_list[i])
                        number.append(-value_list[i + 1])
                    else:
                        number.append(value_list[i])
                return sum(number) if number[-1] > 0 else sum(number[:-1])
        else:
            raise Exception('check your input! give me a string')

    def combine(self, patch):
        if int(patch[0]) == 4:
            for _ in [100, 10, 1]:
                if int(patch) // _ > 0:
                    return self.translator_vs[_] + self.translator_vs[_ * 5]
                    break
        elif int(patch[0]) == 9:
            for _ in [100, 10, 1]:
                if int(patch) // _ > 0:
                    return self.translator_vs[_] + self.translator_vs[_ * 10]
                    break
        elif int(patch[0]) < 4 and int(patch[0]) != 0:
            for _ in [100, 10, 1]:
                if int(patch) // _ > 0:
                    return self.translator_vs[_] * (int(patch) // _)
                    break
        elif int(patch[0]) > 5:
            for _ in [100, 10, 1]:
                if int(patch) // _ > 0:
                    return self.translator_vs[_ * 5] + self.translator_vs[_] * (int(patch) // _ - 5)
                    break
        elif int(patch[0]) == 5:
            for _ in [100, 10, 1]:
                if int(patch) // _ > 0:
                    return self.translator_vs[_ * 5]
                    break
        else:
            return ''


if __name__ == '__main__':
    assert RomanNumerals.to_roman(1) == 'I'
    assert RomanNumerals.to_roman(2708) == 'MMDCCVIII'
    assert RomanNumerals.from_roman('MMLIV') == 2054
    assert RomanNumerals.from_roman('MMVIII') == 2008
