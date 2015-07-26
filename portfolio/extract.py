
from lxml import html
import urllib2
import re
from bs4 import BeautifulSoup


#======= globals ========
bl_url = 'http://www.bloomberg.com/quote/'

#======= return type ======
class Quote(object):
    
    def __init__(self,name,price,currency,change):
        self.name = name
        self.price = price
        self.currency = currency
        self.change = change


#======= determine symbol direction ========
def get_direction(soup):
    if soup.find("div",{"class" : "price-container up"}) is not None:
        return 1 
    elif soup.find("div",{"class" : "price-container down"}) is not None:
        return -1
    else: 
        return 0

#======= get_quote ========
def get_quote(quote):
    url = bl_url + quote 
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(),"lxml")
    #soup = BeautifulSoup(open('/Users/adriaan/Downloads/page.html'),"lxml")
    basic_quote = BeautifulSoup(str(soup.find("div",{"class" : "basic-quote"})),"lxml")
    direction = get_direction(basic_quote)
    name = basic_quote.find("h1", {"class" : "name" }).string.strip()
    price = basic_quote.find("div", { "class" : "price" }).string
    currency = basic_quote.find("div",{"class" : "currency" }).string
    change_str = basic_quote.find("div",{"class" : "change-container"}).contents[1].string
    change = float(change_str.strip()) * direction
    return Quote(name,price,currency,change)






