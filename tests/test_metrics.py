import unittest

from aris_api import metrics

class TestMetrics(unittest.TestCase):
  def test_metric_name(self):
    r = metrics.metric_name('foo', 'bar', 'baz')
    self.assertEqual(r, 'foo_bar_baz')

  def test_value_from_dictionary_keys(self):
    r = metrics.value_from_dictionary_keys(
      {
        'k1': {
          'k2': {
            'k3': 1234
          }
        }
      },
      'k1', 'k2', 'k3'
    )
    self.assertEqual(r, 1234)

  def test_metric_name_value_pair(self):
    d = {
      'k1': {
        'k2': {
          'k3': 1234
        }
      }
    }
    r = metrics.metric_name_value_pair(d, 'foo', 'k1', 'k2', 'k3')
    self.assertEqual(r, ('foo_k1_k2_k3', 1234, {}))

  def test_value_labels(self):
    d = {'foo': 'bar', 'value': 1, 'baz': 'naz'}
    r = metrics.value_labels(d)
    self.assertEqual((1, {'foo': 'bar', 'baz': 'naz'}), r)

  def test_metric_value_labels(self):
    d = {
      'k1': {
        'k2': {
          'k3': [
            {
              'foo': 'bar',
              'value': 1,
            },
            {
              'baz': 'jaz',
              'value': 2,
              'unit': 'u',
              'naz': 'zaz'
            }
          ]
        }
      }
    }
    r = metrics.metric_value_labels(d,'foo', 'k1','k2', 'k3')
    en = 'foo_k1_k2_k3'
    e = [
      (en, 1, {'foo': 'bar'}),
      (en, 2, {'baz': 'jaz', 'unit': 'u', 'naz': 'zaz'})
    ]
    self.assertListEqual(r, e)

  def test_format_labels_dict(self):
    r = metrics.format_labels_dict({'foo': 'bar', 'baz': 'naz'})
    self.assertEqual('{foo="bar", baz="naz"}', r)

if __name__ == '__main__':
    unittest.main()
