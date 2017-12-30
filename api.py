from flask import Flask, jsonify
from aris_api import sb6190

app = Flask(__name__)

@app.route('/')
def main():
  r = sb6190.main()
  return jsonify(r)
