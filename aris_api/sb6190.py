from lxml.html import tostring
from lxml.etree import XPath

import sb
import util

import sys

class SB6190(sb.SB):
  def parse_table(self, table):
    headers = list(table.xpath('.//tr[2]//strong/text()'))
    del headers[2]
    new_info = {k:[] for k in headers}
    infos = super(SB6190, self).parse_table(table).values()
    for i, header in enumerate(headers):
      # skip Channel ID header
      if i == 2:
        continue
      for info in infos:
        channel = info[2]
        value = info[i]
        new_info[header].append({'channel_id': channel, 'value': value})
    return new_info

  def get_info(self):
    tree = self.parse_page_content('cgi-bin/swinfo')
    info = {}
    tr_xpath = XPath("td//text()")
    table = tree.xpath('//table')[0]
    for tr in table.xpath('//tr'):
      tds = list(tr_xpath(tr))
      if tds:
        info[util.make_key_name(tds[0])] = tds[1].strip()
    return info

  def get_address(self):
    return {}

  def get_signal(self):
    tree = self.parse_page_content('cgi-bin/status')
    tables = tree.xpath('//table')
    info = {}
    #startup = self.parse_table(tables[1])
    downstream = self.parse_table(tables[2])
    #upstream = self.parse_table(tables[3])
    return {
      'downstream': downstream
    }

  def get_index(self):
    return {}

def main():
  m = SB6190()
  r = {}
  r['info'] = m.get_info()
  r['address'] = m.get_address()
  r['signal'] = m.get_signal()
  r['index'] = m.get_index()
  return r

if __name__ == '__main__':
  print(main()['info'])
