# Coinbase Prices
Get the current Coinbase prices and save them to a database. If you do not want to build the docker container youself, you can download the prebuilt containers from:
[TBD]

# Usage
```
usage: prices.py [-h] crypto currency

Create a DB of Coinbase prices.

positional arguments:
  crypto      The cryptocurrency coin code.
  currency    The currency of the price.

options:
  -h, --help  show this help message and exit
```

# Example
```
>>> python prices.py BTC USD

Time: 2022-03-30 13:50:00.697442 1648648260
Buy: Price(crypto='BTC', currency='USD', amount=47349.88)
Sell: Price(crypto='BTC', currency='USD', amount=46880.51)
Spot: Price(crypto='BTC', currency='USD', amount=47128.58)

```

# Docker

```
>>> docker build -t coinbase .
>>> docker run coinbase ETH USD

Time: 2022-03-30 13:53:00.627757 1648648380
Buy: Price(crypto='ETH', currency='USD', amount=3392.05)
Sell: Price(crypto='ETH', currency='USD', amount=3357.63)
Spot: Price(crypto='ETH', currency='USD', amount=3379.0)

```
