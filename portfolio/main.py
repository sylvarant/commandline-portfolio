from __future__ import absolute_import

import getopt
import sys

from portfolio.portfolio import Porfolio


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

    p = Porfolio(open(config).read())
    print p


