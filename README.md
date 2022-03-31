# Coinbase Prices
Get the current Coinbase prices and save them to a database. If you do not want to build the docker container youself, you can download the prebuilt containers from:
https://hub.docker.com/repository/docker/minormending/pycoinbase-prices

# Usage
```
usage: prices.py [-h] [--db DB] currency crypto

Create a DB of Coinbase prices.

positional arguments:
  currency    The currency of the price.
  crypto      The cryptocurrency coin code.

options:
  -h, --help  show this help message and exit
  --db DB     Database location.
```

# Example
```
>>> python prices.py USD BTC

Time: 2022-03-30 13:50:00.697442 1648648260
Buy: Price(crypto='BTC', currency='USD', amount=47349.88)
Sell: Price(crypto='BTC', currency='USD', amount=46880.51)
Spot: Price(crypto='BTC', currency='USD', amount=47128.58)

```

# Docker

```
>>> docker build -t coinbase .
>>> docker run coinbase USD ETH

Time: 2022-03-30 13:53:00.627757 1648648380
Buy: Price(crypto='ETH', currency='USD', amount=3392.05)
Sell: Price(crypto='ETH', currency='USD', amount=3357.63)
Spot: Price(crypto='ETH', currency='USD', amount=3379.0)

>> docker run coinbase -v /opt/coinbase.db:/app/prices.sqlite USD ETH

Time: 2022-03-30 13:53:00.627757 1648648380
Buy: Price(crypto='ETH', currency='USD', amount=3392.05)
Sell: Price(crypto='ETH', currency='USD', amount=3357.63)
Spot: Price(crypto='ETH', currency='USD', amount=3379.0)

```
