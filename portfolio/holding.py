from __future__ import absolute_import
import re

from portfolio.extract import get_quote
from portfolio.interface import str_color, num_color

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
    self.day_gain = quote.gain
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

  # row to the interface
  def row(self,form):
    def is_float(form):
      match = re.search('f$',form)
      return match 
    # create alignment
    def align_fl(form,color):
      sign = (1 if (re.search('^\%\+',form)) else 0)
      match = re.search('([0-9]+)\.([0-9]+)f$',form)
      ansii = (len('\x1b[1m\x1b[32m') + len('\x1b(B\x1b[m\x1b(B\x1b[m')) if color else 0
      if match:
        return ("%" + str(int(match.group(1)) + int(match.group(2)) + ansii + sign + 1) + "s") 
      else :
        return form

    # process format
    nform = map((lambda x: align_fl(x,False)),form[:2]) + map((lambda x: align_fl(x,False)),form[2:])
    finalform = " ".join(nform);

    # process arguments
    args = [("("+self.currency+")"),self.day_gain]
    if self.lots is not None:
      args.append(self.gain)
    args = [(str_color((x % y),y) if is_float(x) else y) for x,y in zip(form[2:],args)]
    return finalform % tuple([self.name,self.last_price] + args)
     
