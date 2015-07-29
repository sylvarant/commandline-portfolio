from __future__ import absolute_import

from portfolio.extract import get_quote


#======================================
# Exceptions
#======================================

class HoldingError(Exception):

  def __init__(self,note):
    self.note = note

  def __str__(self):
    return "Failed to retrieve Holding: " + self.note


#== Class =============================
#   * Holding
#   -- A financial symbol held in lots
#======================================
class Holding(object):

  def __init__(self,holding):
    if not holding.has_key('quote'):
      raise HoldingError("Quote missing")
    self.name = holding['quote']
    quote = get_quote(self.name)
    self.last_price = quote.price
    self.currency = quote.currency
    self.day_gain = quote.change
    self.lots = None
    self.gain = 0
    self.value = 0
    if holding.has_key('lots'):
      self.lots = holding['lots']
      for lot in self.lots:
        if not (lot.has_key("Amount") and lot.has_key("Value")):
          raise HoldingError("Missing attribute in lots")
        self.gain += float(lot["Amount"]) * (self.last_price - float(lot["Value"])) 
        self.value += float(lot["Amount"]) * self.last_price


  def __str__(self):
    today = (self.name + " :: " + str(self.last_price) + " (" + self.currency + ")"
    + " :: " + str(self.day_gain))
    if self.lots is not None:
      today = today + " :: " + str(self.gain) + " (" + self.currency + ")"
    return today

