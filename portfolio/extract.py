from lxml import html
import urllib2
import re
from bs4 import BeautifulSoup


#======= globals ========
bl_url = 'http://www.bloomberg.com/quote/'
headers = { 'User-Agent' : 
#  'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5'}
  'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19' }

#== Class =============================
#   * Quote
#   -- A collection of finance data
#======================================
class Quote(object):

  def __init__(self,name,price,currency,gain):
    self.name = name
    self.price = price
    self.currency = currency
    self.gain = gain


#======= determine symbol direction ========
def get_direction(soup):
  if soup.find("div",{"class" : "price-container up"}) is not None:
    return 1 
  elif soup.find("div",{"class" : "price-container down"}) is not None:
    return -1
  else: 
    return 0


#======= Check that bloomberg has the quote ========
def is_quote(quote):
  url = bl_url + quote 
  req = urllib2.Request(url, None, headers)
  req.headers['Range'] = 'bytes=%s-%s' % (0, 1024) # TODO does not work
  page = urllib2.urlopen(req)
  soup = BeautifulSoup(page.read(),"lxml")
  res = soup.find("div",{"class" : "basic-quote"})
  if res is None:
    return False
  else:
    return True


#======= Check that bloomberg has the currency ========
def is_currency(curr):
  quote = curr
  match = re.search(':CUR',quote)
  if match is None:
    quote = quote + ':CUR'  
  return is_quote(quote)

#======= get_quote ========
def get_quote(quote):
  url = bl_url + quote 
  req = urllib2.Request(url, None, headers)
  page = urllib2.urlopen(req)
  soup = BeautifulSoup(page.read(),"lxml")
  #soup = BeautifulSoup(open('/Users/adriaan/Downloads/page.html'),"lxml")
  basic_quote = BeautifulSoup(str(soup.find("div",{"class" : "basic-quote"})),"lxml")
  direction = get_direction(basic_quote)
  name = basic_quote.find("h1", {"class" : "name" }).string.strip()
  price = float(basic_quote.find("div", { "class" : "price" }).string)
  currency = basic_quote.find("div",{"class" : "currency" }).string
  change_str = basic_quote.find("div",{"class" : "change-container"}).contents[1].string
  gain = float(change_str.strip()) * direction
  return Quote(name,price,currency,gain)


