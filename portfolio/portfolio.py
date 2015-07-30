from __future__ import absolute_import

import json
import re
from portfolio.extract import is_currency, get_quote
from portfolio.holding import Holding
from portfolio.interface import str_color

#======================================
# Exceptions
#======================================

class IncorrectConfig(Exception):

  def __init__(self,note):
    self.note = note

  def __str__(self):
    return "Failed to parse config: " + self.note


#==== convert to new currency =====
def to_curr(amount,old,new):
  if old == new :
    return amount
  quote = get_quote(old + new + ':CUR')
  return (quote.price * float(amount))
      


#== Class =============================
#   * Portfolio
#   -- A collection of holdings 
#   -- That provides a certain earning
#======================================
class Portfolio(object):

  def __init__(self,config):
    decode = None 
    try:
      decode = json.loads(config)
    except: 
      raise IncorrectConfig("Flawed json")
    if not decode.has_key('currency'):
      raise IncorrectConfig('Currency not defined') 
    elif not is_currency(decode['currency']):
      raise IncorrectConfig('Unknown currency')
    elif not (decode.has_key('holdings') and len(decode['holdings']) > 0):
      raise IncorrectConfig('No holdings defined') 
    m = re.match("(\w+)(:.*|$)", decode['currency'])
    self.currency = m.groups()[0]
    self.holdings = []
    for holding in decode['holdings']:
      self.holdings.append(Holding(holding))
    gains = map(lambda x: to_curr(x.gain,x.currency,self.currency),self.holdings)
    values = map(lambda x: to_curr(x.value,x.currency,self.currency),self.holdings)
    self.gain = reduce((lambda x,y: x + y),gains)
    self.value = reduce((lambda x,y: x + y),values)

  def earnings_statement(self):
    return ("Total value "+ str(self.value) +" of which is earnings: " + str_color(self.gain) + " (" + self.currency + ')')

  def __str__(self):
    str_list = []
    for holding in self.holdings:
      str_list.append(str(holding))
    str_list.append(self.earnings_statement())
    out_str = "\n".join(str_list)
    return out_str

      
    

