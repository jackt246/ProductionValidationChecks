import unittest
from unittest.mock import patch
from file_import import VaFileFinder


class TestVaFileFinder(unittest.TestCase):

    def setUp(self):
        self.finder = VaFileFinder('/test/path')

    @patch('os.path.exists')
    def test_find_va_file_4_digit_exists(self, mock_exists):
        mock_exists.return_value = True
        result = self.finder.find_va_file('EMD-1234')
        self.assertEqual(result, '/test/path/12/1234/va/checks/1234_all_checks.json')

    @patch('os.path.exists')
    def test_find_va_file_5_digit_exists(self, mock_exists):
        mock_exists.return_value = True
        result = self.finder.find_va_file('EMD-12345')
        self.assertEqual(result, '/test/path/12/3/12345/va/checks/12345_all_checks.json')

    @patch('os.path.exists')
    def test_find_va_file_nonexistent_file(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(ValueError) as context:
            self.finder.find_va_file('EMD-1234')
        self.assertIn('file not found', str(context.exception))

    def test_find_va_file_invalid_format(self):
        with self.assertRaises(ValueError) as context:
            self.finder.find_va_file('INVALID-1234')
        self.assertIn('Entry must be in the format EMD-XXXX or EMD-XXXXX', str(context.exception))

    def test_find_va_file_invalid_length(self):
        with self.assertRaises(ValueError) as context:
            self.finder.find_va_file('EMD-123')
        self.assertIn('Entry must be in the format EMD-XXXX or EMD-XXXXX', str(context.exception))


if __name__ == '__main__':
    unittest.main()
