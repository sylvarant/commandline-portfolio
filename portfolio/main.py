#!/usr/bin/env python

import getopt
import sys
import json

from portfolio.holding import Holding


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
    
    for holding in decode['holdings']:
        h = Holding(holding)
        print h



