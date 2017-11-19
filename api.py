from flask import Flask, jsonify, request
from aris_api import sb6141, metrics as m

app = Flask(__name__)

@app.route('/')
def main():
  r = sb6141.stats()
  return jsonify(r)

# # HELP http_requests_total The total number of HTTP requests.
# # TYPE http_requests_total counter
# http_requests_total{method="post",code="200"} 1027 1395066363000
@app.route('/metrics')
def metrics():
  headers = request.headers
  r = sb6141.stats()
  return m.line_break(headers).join(
    m.make_metrics(r, 'sb6141', headers)
  )
