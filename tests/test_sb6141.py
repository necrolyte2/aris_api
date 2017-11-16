from os.path import *
import unittest
import os
from unittest.mock import MagicMock
import datetime

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

  def test_parse_updtime(self):
    r = self.object.parse_uptime('0 days 2h:43m:49s')
    self.assertEqual(r, datetime.timedelta(0, 9829))

if __name__ == '__main__':
    unittest.main()
