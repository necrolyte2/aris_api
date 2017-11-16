from flask import Flask, jsonify
from aris_api import sb6141

app = Flask(__name__)

@app.route('/')
def main():
  r = sb6141.main()
  return jsonify(r)
