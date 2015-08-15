from __future__ import absolute_import

import json
import re
from portfolio.extract import is_currency, get_quote
from portfolio.holding import Holding
from portfolio.interface import str_color, num_color

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

  def earnings_statement(self,color):
    value = ("%.2f" % self.value) if not color else str_color(("%.2f" % self.value),self.gain)
    gain  = ("%+.2f" % self.gain) if not color else str_color(("%+.2f" % self.gain),self.gain)
    return ("Total value: "+ value + " (" + self.currency + ')' 
      +" -- Total Profit: " + gain + " (" + self.currency + ')') 

  def __str__(self):
    str_list = []
    for holding in self.holdings:
      str_list.append(str(holding))
    str_list.append(self.earnings_statement())
    out_str = "\n".join(str_list)
    return out_str

  def print_table(self): 

    # compute largest string size
    def max_string_size(ls,noted):
      prefix = "%-" if noted else "%"
      return prefix + str(len(reduce((lambda x,y: (x if (len(x) > len(y)) else y)),ls))) + "s"

    # compute largest decimal size of float - after point set at 2
    def max_fl_size(ls,noted):
      def decimals(fl):
        pfl = fl if fl > 0 else -fl
        if pfl < 10 :
          return (1 if fl > 0 else 2)
        else :
          return 1 + decimals((fl/10))
      prefix = "%+" if noted else "%"
      return prefix + str(decimals(reduce(lambda x,y: (x if decimals(x) > decimals(y) else y) ,ls))) + ".2f" 

    # compute the format
    namef  = max_string_size(map(lambda x: x.name,self.holdings),True)
    pricef = max_fl_size(map(lambda x: x.last_price,self.holdings),False)
    currf  = max_string_size(map(lambda x: ("(" + x.currency + ")"),self.holdings),False) 
    percf  = max_fl_size(map(lambda x: x.day_gain,self.holdings),True)
    gainf  = max_fl_size(map(lambda x: x.gain, self.holdings),True)
    form   = [namef, pricef, currf, percf]
    for holding in self.holdings:
      cform = list(form)
      if holding.lots is not None:
        cform.append(gainf)
      print holding.row(cform) 
    print "".join(map((lambda x: "-"),range(len(self.earnings_statement(False)))))
    print self.earnings_statement(True) # todo
    

