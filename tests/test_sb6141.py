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
    self.assertEqual(r, 9829)

  def test_parse_value_unit(self):
    r = self.object.parse_value_unit('12345 unit')
    self.assertListEqual([12345, 'unit'], r)

  def test_value_convert_list(self):
    x = [
      {'foo': "1", 'value': '1234 unit'},
      {'bar': "1", 'value': '5678 unit'},
    ]
    self.object.value_convert_list(x)
    self.assertEqual(x[0], {'foo': '1', 'value': 1234.0, 'unit': 'unit'})
    self.assertEqual(x[1], {'bar': '1', 'value': 5678.0, 'unit': 'unit'})

if __name__ == '__main__':
    unittest.main()
