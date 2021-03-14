import unittest
from Training_classes.Roman_Numerals_Helper import RomanNumerals


class MyTestCase(unittest.TestCase):

    def test_to_roman_first_20(self):
        self.assertEqual(RomanNumerals.to_roman(1), 'I')
        self.assertEqual(RomanNumerals.to_roman(3), 'III')
        self.assertEqual(RomanNumerals.to_roman(4), 'IV')
        self.assertEqual(RomanNumerals.to_roman(5), 'V')
        self.assertEqual(RomanNumerals.to_roman(9), 'IX')
        self.assertEqual(RomanNumerals.to_roman(17), 'XVII')
        self.assertEqual(RomanNumerals.to_roman(20), 'XX')

    def test_to_roman(self):
        self.assertEqual(RomanNumerals.to_roman(499), 'CDXCIX')
        self.assertEqual(RomanNumerals.to_roman(1), 'I')
        self.assertEqual(RomanNumerals.to_roman(2708), 'MMDCCVIII')

    def test_from_roman(self):
        self.assertEqual(RomanNumerals.from_roman('MMLIV'), 2054)
        self.assertEqual(RomanNumerals.from_roman('MCMLIV'), 1954)
        self.assertEqual(RomanNumerals.from_roman('MMVIII'), 2008)

    def test_from_roman_single_letter(self):
        self.assertEqual(RomanNumerals.from_roman('I'), 1)


if __name__ == '__main__':
    unittest.main()
