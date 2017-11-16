from flask import Flask, jsonify
from aris_api import sb6141

app = Flask(__name__)

@app.route('/')
def main():
  m = sb6141.Modem()
  r = {}
  r['info'] = m.get_info()
  r['address'] = m.get_address()
  r['signal'] = m.get_signal()
  return jsonify(r)
