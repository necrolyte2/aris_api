import re

import requests
import dateparser
import time
from datetime import datetime, timedelta
from lxml.html import tostring

import modem
import util

class SB6141(modem.Modem):
  def get_info(self):
    tree = self.parse_page_content('cmHelpData.htm')
    t = tree.xpath('//table/tbody')[0]
    info = {}
    for x in tree.xpath('//table')[0].xpath('//tr/td')[0]:
      s = str(tostring(x)).replace('<br>','').strip()
      s = s.split(':', 1)
      if s[0] != '':
        info[util.make_key_name(s[0])] = s[1].strip()
    return info

  def get_address(self):
    tree = self.parse_page_content('cmAddressData.htm')
    x = tree.xpath('//table')[0]
    d = {}
    k = None
    for a in x.xpath('.//td/text()'):
      if k is None:
        k = util.make_key_name(a)
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

  def get_index(self):
    tree = self.parse_page_content('indexData.htm')
    tables = tree.xpath('//table')
    info = {
      'task': self.parse_task_table(tables[0]),
      'operation': self.parse_operation_table(tables[1])
    }
    return info

  def parse_task_table(self, table):
    return {k: {v[0]: 1} for k,v in self.parse_table(table).items()}

  def parse_uptime(self, uptime):
    p = '(\d+) days (\d+)h:(\d+)m:(\d+)s'
    r = re.match(p, uptime)
    v = [int(x) for x in r.groups()]
    return timedelta(days=v[0], hours=v[1], minutes=v[2], seconds=v[3]).total_seconds()

  def parse_operation_table(self, table):
    x = self.parse_table(table)
    return {
      'current_time_and_date': time.mktime(dateparser.parse(x['current_time_and_date'][0]).timetuple()),
      'system_up_time': self.parse_uptime(x['system_up_time'][0])
    }

  def create_channel_info(self, parsed_table):
    channels = parsed_table['channel_id'] 
    keys = filter(lambda x: x != 'channel_id', parsed_table.keys())
    info = {k:[] for k in keys}
    for i, channel in enumerate(channels):
      for k in keys:
        info[k].append({'channel_id':channel, 'value': parsed_table[k][i]})
    return info

  def parse_downstream(self, table):
    return self.create_channel_info(self.parse_table(table))

  def parse_upstream(self, table):
    return self.create_channel_info(self.parse_table(table))

  def parse_signal_stats(self, table):
    return self.create_channel_info(self.parse_table(table))

def main():
  m = SB6141()
  r = {}
  r['info'] = m.get_info()
  r['address'] = m.get_address()
  r['signal'] = m.get_signal()
  r['index'] = m.get_index()
  return r

if __name__ == '__main__':
  print(main()['index'])
