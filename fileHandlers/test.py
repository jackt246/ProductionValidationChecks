import fileImport
import unittest
class TestVAFileFinder(unittest.TestCase):
    def setUp(self):
        self.finder = fileImport.VaFileFinder('/mock/path')

    def test_find_va_file_4_digits(self):
        result = self.finder.find_va_file('EMD-1234')
        expected = '/mock/path/12/EMD-1234'
        self.assertEqual(result, expected)

    def test_find_va_file_5_digits(self):
        result = self.finder.find_va_file('EMD-12345')
        expected = '/mock/path/12/3/EMD-12345'
        self.assertEqual(result, expected)

    def test_find_va_file_invalid_format(self):
        with self.assertRaises(ValueError) as context:
            self.finder.find_va_file('EMD-123')
        self.assertEqual(str(context.exception), 'Entry must be in the format EMD-XXXX or EMD-XXXXX where X is an integer.')

    def test_find_va_file_non_integer(self):
        with self.assertRaises(ValueError) as context:
            self.finder.find_va_file('EMD-1234A')
        self.assertEqual(str(context.exception), 'Entry must be in the format EMD-XXXX or EMD-XXXXX where X is an integer.')

    def test_find_va_file_long_entry(self):
        with self.assertRaises(ValueError) as context:
            self.finder.find_va_file('EMD-123456')
        self.assertEqual(str(context.exception), 'Entry must be in the format EMD-XXXX or EMD-XXXXX where X is an integer.')

    def test_find_va_file_too_short(self):
        with self.assertRaises(ValueError) as context:
            self.finder.find_va_file('EMD-12')
        self.assertEqual(str(context.exception), 'Entry must be in the format EMD-XXXX or EMD-XXXXX where X is an integer.')

if __name__ == '__main__':
    unittest.main()