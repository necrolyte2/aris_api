# aris_api

Super simply silly api for ARIS Surfboard modem to get information by
scraping it from the html pages the modem has.

It also exposes `/metrics` as a prometheus metrics endpoint

## Run Flask API

```
docker run --rm -it -p 5000:5000 --name aris_api testing
```

## Build locally

```
docker build -t whatever .
```

## Test

```
python -m unittest tests/*.py
```
