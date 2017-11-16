import re

import requests
from lxml import html
from lxml.html import tostring
# http://192.168.100.1/cmHelp.htm

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

  def get_info(self):
    tree = self.parse_page_content('cmHelpData.htm')
    t = tree.xpath('//table/tbody')[0]
    info = {}
    for x in tree.xpath('//table')[0].xpath('//tr/td')[0]:
      s = str(tostring(x)).replace('<br>','').strip()
      s = s.split(':', 1)
      if s[0] != '':
        info[make_key_name(s[0])] = s[1].strip()
    return info

  def get_address(self):
    tree = self.parse_page_content('cmAddressData.htm')
    x = tree.xpath('//table')[0]
    d = {}
    k = None
    for a in x.xpath('.//td/text()'):
      if k is None:
        k = make_key_name(a)
        d[a] = None
      else:
        d[k] = a
        k = None
    return d

  def get_signal(self):
    tree = self.parse_page_content('cmSignalData.htm')
    tables = tree.xpath('//table')
    info = {}
    info['downstream'] = self.parse_downstream(tables[0])
    info['upstream'] = self.parse_upstream(tables[2])
    info['signal_stats'] = self.parse_signal_stats(tables[3])
    return info

  def parse_signal_table(self, table):
    info = {}
    for tr in table.xpath('.//tr'):
      k = None
      for td in tr.xpath('.//td/text()'):
        td = td.encode('ascii', 'ignore').strip()
        if k is None:
          k = make_key_name(td)
          info[k] = []
        else:
          info[k].append(td.strip())
    return info

  def create_channel_info(self, parsed_table):
    channels = parsed_table['channel_id'] 
    keys = filter(lambda x: x != 'channel_id', parsed_table.keys())
    info = {k:[] for k in keys}
    for i, channel in enumerate(channels):
      for k in keys:
        info[k].append({'channel_id':channel, 'value': parsed_table[k][i]})
    return info

  def parse_downstream(self, table):
    return self.create_channel_info(self.parse_signal_table(table))

  def parse_upstream(self, table):
    return self.create_channel_info(self.parse_signal_table(table))

  def parse_signal_stats(self, table):
    return self.create_channel_info(self.parse_signal_table(table))

def make_key_name(key):
  return key.strip().lower().replace(' ', '_')
