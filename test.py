import unittest
import pdfstitch


class TestArgParse(unittest.TestCase):
    def test_file_args(self):
        pdfstitch.merge_docs('test_output.pdf', './data/test.json')


if __name__ == '__main__':
    unittest.main()
