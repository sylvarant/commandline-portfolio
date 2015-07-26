
import unittest
from portfolio.extract import *

class TestQuote(unittest.TestCase):

    def setUp(self):
        self.quote = get_quote('AMZN:US')

    def test_name(self):
      self.assertEqual(self.quote.name, 'Amazon.com Inc')


if __name__ == '__main__':
    unittest.main()

# vim: ft=python
