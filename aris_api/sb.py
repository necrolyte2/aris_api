import modem
import util

from lxml.html import tostring

class SB(modem.Modem):
  def parse_table(self, table):
    info = {}
    for tr in table.xpath('.//tr'):
      k = None
      for td in tr.xpath('.//td/text()'):
        td = td.encode('ascii', 'ignore').strip()
        if k is None:
          k = util.make_key_name(td)
          info[k] = []
        else:
          info[k].append(td.strip())
    return info

  def parse_downstream(self, table):
    return self.create_channel_info(self.parse_table(table))
