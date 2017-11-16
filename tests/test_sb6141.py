from os.path import *
import unittest
import os
from unittest.mock import MagicMock

from aris_api import sb6141

FIXTURES_DIR = join(dirname(abspath(__file__)), 'fixtures')

def fixtures():
  return {f:join(FIXTURES_DIR, f) for f in os.listdir(FIXTURES_DIR)}

def load_fixture(path):
  html = None
  with open(path) as fh:
    html = fh.read()
  return html

def load_fixtures():
  return {f:load_fixture(p) for f, p in fixtures().items()}

FIXTURES = load_fixtures()

class TestModem(unittest.TestCase):
  def setUp(self):
    self.object = sb6141.Modem()
    self.info_page = MagicMock(return_value=FIXTURES['cmHelpData.htm'])
    self.page = MagicMock(return_value=FIXTURES['cmHelpData.htm'])
    self.object.get_page_content = self.info_page

  def test_gets_info(self):
    self.object.get_info()

  def test_get_address(self):
    self.object.get_address()

if __name__ == '__main__':
    unittest.main()
