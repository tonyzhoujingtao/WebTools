import unittest
from src.simple_filter import SimpleFilter
from src.randoms import random_string
import os


class TestSimpleFilter(unittest.TestCase):
    def setUp(self):
        self.random_file_name = random_string(3)

    def test_touch_open(self):
        simple_filter = SimpleFilter(self.random_file_name)

        item = 'one'
        filtered_item = simple_filter.filter(item)
        self.assertEquals(item, filtered_item)

        item = 'two'
        filtered_item = simple_filter.filter(item)
        self.assertEquals(item, filtered_item)

        item = 'two'
        filtered_item = simple_filter.filter(item)
        self.assertNotEquals(item, filtered_item)

    def tearDown(self):
        os.remove(self.random_file_name)


if __name__ == '__main__':
    unittest.main()
