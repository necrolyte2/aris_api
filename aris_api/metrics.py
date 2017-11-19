def format_labels_dict(labels):
  labels_str = []
  for k,v in labels.items():
    labels_str.append('{}="{}"'.format(k,v))
  return '{' + ', '.join(labels_str) + '}'

def make_metric(metric_name_value, metric_type, headers, create_header=True):
  lines = []
  if create_header:
    lines.append('# HELP {}'.format(metric_name_value[0]))
    lines.append('# Type {} {}'.format(metric_name_value[0], metric_type))
  lines.append(
    '{}{} {}'.format(
      metric_name_value[0],
      format_labels_dict(metric_name_value[2]),
      metric_name_value[1]
    )
  )
  return line_break(headers).join(lines)

def metric_name_value_pair(d, base_name, *args):
  name = metric_name(base_name, *args)
  value = value_from_dictionary_keys(d, *args)
  return (name, value, {})

def metric_name(base_name, *args):
  return base_name + '_' + '_'.join(args)

def value_from_dictionary_keys(d, *args):
  value = d
  for key in args:
    value = value[key]
  return value

def line_break(headers):
  accept = headers.get('accept')
  lb = '\n'
  if 'text/html' in accept:
    lb = '<br>'
  return lb

def make_metrics(stats, base_name, headers):
  metrics = []
  metrics.append(
    make_metric(
      metric_name_value_pair(stats, base_name, 'index', 'operation', 'current_time_and_date'),
      'Counter',
      headers
    )      
  )
  metrics.append(
    make_metric(
      metric_name_value_pair(stats, base_name, 'index', 'operation', 'system_up_time'),
      'Counter',
      headers
    )
  )
  metrics += create_metric(
    stats, base_name, 'Gauge', headers, 'signal', 'downstream', 'frequency'
  )
  metrics += create_metric(
    stats, base_name, 'Gauge', headers, 'signal', 'downstream', 'power_level'
  )
  metrics += create_metric(
    stats, base_name, 'Gauge', headers, 'signal', 'upstream', 'frequency'
  )
  metrics += create_metric(
    stats, base_name, 'Gauge', headers, 'signal', 'upstream', 'power_level'
  )
  metrics += create_metric(
    stats, base_name, 'Gauge', headers, 'signal', 'upstream', 'ranging_service_id'
  )
  metrics += create_metric(
    stats, base_name, 'Gauge', headers, 'signal', 'upstream', 'symbol_rate'
  )
  metrics += create_metric(
    stats, base_name, 'Gauge', headers, 'signal', 'downstream', 'signal_to_noise_ratio'
  )
  metrics += create_metric(
    stats, base_name, 'Counter', headers, 'signal', 'signal_stats', 'total_correctable_codewords'
  )
  metrics += create_metric(
    stats, base_name, 'Counter', headers, 'signal', 'signal_stats', 'total_uncorrectable_codewords'
  )
  metrics += create_metric(
    stats, base_name, 'Counter', headers, 'signal', 'signal_stats', 'total_unerrored_codewords'
  )
  return metrics

def value_labels(d):
  x = {}
  x.update(d)
  value = x['value']
  del x['value']
  return (value, x)

def create_metric(d, base_name, metric_type, headers, *args):
  first = True
  metrics = []
  for x in metric_value_labels(d, base_name, *args):
    metrics.append(
      make_metric(x, metric_type, headers, first)
    )
    if first:
      first = False
  return metrics
  
def metric_value_labels(d, base_name, *args):
  name = metric_name(base_name, *args)
  items = value_from_dictionary_keys(d, *args)
  values = []
  for item in items:
    x = value_labels(item)
    values.append((name, x[0], x[1]))
  return values
