
import unittest
from portfolio.portfolio import Portfolio, IncorrectConfig, to_curr

class TestPortfolio(unittest.TestCase):

  def test_to_curr(self):
    self.assertEqual(to_curr(100,'EUR','EUR'),100)
    self.assertTrue(to_curr(100,'EUR','USD') != 0) 


  def test_construction(self):
    self.assertRaises(IncorrectConfig,Portfolio,'{')
    self.assertRaises(IncorrectConfig,Portfolio,'{}') 
    self.assertRaises(IncorrectConfig,Portfolio,'{"currency" : "Amero"}')
    self.assertRaises(IncorrectConfig,Portfolio,'{"currency" : "EUR"}') 
    port = Portfolio('{"currency" : "EUR", "holdings" : [ { "quote" : "AMZN:US" } ] }')
    self.assertTrue(port.gain == 0)

if __name__ == '__main__':
  unittest.main()

