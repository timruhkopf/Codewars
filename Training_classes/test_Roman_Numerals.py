import unittest
from Training_classes.Roman_Numerals_Helper import RomanNumerals


class MyTestCase(unittest.TestCase):

    def test_something(self):
        self.assertEqual(RomanNumerals.to_roman(1), 'I')
        self.assertEqual(RomanNumerals.to_roman(2708), 'MMDCCVIII')

    def test_from_roman(self):
        self.assertEqual(RomanNumerals.from_roman('MMLIV'), 2054)
        self.assertEqual(RomanNumerals.from_roman('MMVIII'), 2008)


if __name__ == '__main__':
    unittest.main()
