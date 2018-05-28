import unittest
from src import files, randoms
import os


class TestFiles(unittest.TestCase):
    def setUp(self):
        self.random_file_name = randoms.random_string(5)

    def test_touch_open(self):
        read_file = files.touch_open(self.random_file_name, "r")
        lines = read_file.readlines()
        read_file.close()
        self.assertFalse(lines)

    def tearDown(self):
        os.remove(self.random_file_name)


if __name__ == '__main__':
    unittest.main()
