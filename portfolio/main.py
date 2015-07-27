#!/usr/bin/env python

import getopt
import sys
import json

from portfolio.extract import is_currency
from portfolio.holding import Holding


#======================================
# Exceptions
#======================================

class IncorrectConfig(Exception):

  def __init__(self,note):
    self.note = note

    def __str__(self):
      return "Failed to parse config: " + self.note


#======= usage ========
def usage():
  usage = 'portfolio -[hs|...]'
  print 'Usage:', usage
  sys.exit(2)


#======= main ========
def main(argv):

  config = "~/.portfolio.json"

  # cli arguments
  try:
    opts, args = getopt.getopt(argv,"hs:",[])
  except getopt.GetoptError:
    usage()

  for opt, arg in opts:
    if opt == '-h':
      usage()
    elif opt == '-s':
      config = arg

  # read in json 
  # todo clean up warning
  decode = json.loads(open(config).read())
  if not decode.has_key('currency'):
    raise IncorrectConfig('Currency not defined') 
  elif not is_currency(decode['currency']):
    raise IncorrectConfig('Unknown currency')
  elif not (decode.has_key('holdings') and len(decode['holdings']) > 0):
    raise IncorrectConfig('No holdings defined') 

  curr =  decode['currency']
  for holding in decode['holdings']:
    h = Holding(holding,curr)
    print h



