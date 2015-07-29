
import unittest
from portfolio.extract import *

class TestExtract(unittest.TestCase):

  def test_name(self):
    quote = get_quote('AMZN:US')
    self.assertEqual(quote.name, 'Amazon.com Inc')

  def test_is_currency(self):
    self.assertTrue(is_currency('USD'))
    self.assertTrue(is_currency('USD:CUR'))
    self.assertFalse(is_currency('Maximo'))


if __name__ == '__main__':
  unittest.main()

