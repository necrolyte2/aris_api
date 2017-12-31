import sb6141 as api

from prometheus_client import start_http_server, Counter, Gauge
import random
import time

if __name__ == '__main__':
    print("Fetching metrics from modem")
    modem_stats = api.stats()
    # Start up the server to expose the metrics.
    print("Starting server on port 8000")
    start_http_server(8000)
