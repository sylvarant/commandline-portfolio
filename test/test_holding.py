
import unittest
from portfolio.holding import Holding, HoldingError

class TestHolding(unittest.TestCase):

  def test_construction(self):
    self.assertRaises(HoldingError,Holding,{})
    self.assertRaises(HoldingError,Holding,{"quote" : "BAC:US", "lots" : [ { } ] })
    hold = Holding({"quote" : "BAC:US", "lots" : [ {"Amount" : 10, "Value" : 0 } ] })
    self.assertTrue(hold.gain > 0)

if __name__ == '__main__':
  unittest.main()

