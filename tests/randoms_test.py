import unittest
from src import randoms

class TestRandoms(unittest.TestCase):
    def setUp(self):
        self.length = 5
        self.times = 1000
        self.generated_strings = set([])

    def test_random_strings(self):
        for t in range(self.times):
            random_string = randoms.random_string(self.length)
            self.assertFalse(random_string in self.generated_strings)
            self.generated_strings.add(random_string)

if __name__ == '__main__':
    unittest.main()
