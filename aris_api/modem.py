import requests
from lxml import html

class Modem(object):
  def __init__(self, address='192.168.100.1', scheme='http'):
    self.address = address
    self.scheme = scheme

  def get_page(self, path):
    r = requests.get(self.scheme + '://' + self.address + '/' + path)
    return r

  def get_page_content(self, path):
    return self.get_page(path).content

  def parse_page_content(self, path):
    page = self.get_page_content(path)
    return html.fromstring(page)
