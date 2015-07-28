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
    self.day_change = quote.change
    self.lots = None
    self.change = 0
    if holding.has_key('lots'):
      self.lots = holding['lots']
      for lot in self.lots:
        if not (lot.has_key("Amount") and lot.has_key("Value")):
          raise HoldingError("Missing attribute in lots")
        self.change += float(lot["Amount"]) * (self.last_price - float(lot["Value"])) 


  def __str__(self):
    today = (self.name + " :: " + str(self.last_price) + " (" + self.currency + ")"
    + " :: " + str(self.day_change))
    if self.lots is not None:
      today = today + " :: " + str(self.change) + " (" + self.currency + ")"
    return today

