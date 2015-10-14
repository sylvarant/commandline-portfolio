from __future__ import absolute_import

import getopt
import sys

from portfolio.portfolio import Portfolio


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
  
  try: 
    p = Portfolio(open(config).read())
    p.print_table()
  except IOError:
    print 'portfolio file not found!'
    sys.exit(1)


