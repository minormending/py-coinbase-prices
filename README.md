# Coinbase Prices
Get the current Coinbase buy/sell/spot prices and save them to a database. Coinbase's historical prices API only provides a single the spot price for a day; however, cyrpto prices can be extremely volatile hour by hour. The project allows you to build a database of hourly (or by minute) prices for your own models (without the need for an API key).

If you do not want to build the docker container youself, you can download the prebuilt containers from:
https://hub.docker.com/repository/docker/minormending/pycoinbase-prices

# Usage
```
usage: prices.py [-h] [--db DB] currency cryptos [cryptos ...]

Create a DB of Coinbase prices.

positional arguments:
  currency    The currency of the price.
  cryptos     The cryptocurrency coin code.

options:
  -h, --help  show this help message and exit
  --db DB     Database location.
```

# Example
```
>>> python prices.py USD BTC SOL

Time: 2022-03-30 13:50:00.697442 1648648260
Buy: Price(crypto='BTC', currency='USD', amount=47349.88)
Sell: Price(crypto='BTC', currency='USD', amount=46880.51)
Spot: Price(crypto='BTC', currency='USD', amount=47128.58)

Time: 2022-03-30 13:50:00.697442 1648648260
Buy: Price(crypto='SOL', currency='USD', amount=137.74)
Sell: Price(crypto='SOL', currency='USD', amount=136.29)
Spot: Price(crypto='SOL', currency='USD', amount=137.05)
```

# Docker

```
>>> docker build -t coinbase .
>>> docker run coinbase USD ETH ADA

Time: 2022-03-30 13:53:00.627757 1648648380
Buy: Price(crypto='ETH', currency='USD', amount=3392.05)
Sell: Price(crypto='ETH', currency='USD', amount=3357.63)
Spot: Price(crypto='ETH', currency='USD', amount=3379.0)

Time: 2022-03-30 13:53:00.627757 1648648380
Buy: Price(crypto='ADA', currency='USD', amount=1.19)
Sell: Price(crypto='ADA', currency='USD', amount=1.17)
Spot: Price(crypto='ADA', currency='USD', amount=1.1791)

>> docker run coinbase -v /opt/coinbase.db:/app/prices.sqlite USD ETH ADA

Time: 2022-03-30 13:53:00.627757 1648648380
Buy: Price(crypto='ETH', currency='USD', amount=3392.05)
Sell: Price(crypto='ETH', currency='USD', amount=3357.63)
Spot: Price(crypto='ETH', currency='USD', amount=3379.0)

Time: 2022-03-30 13:53:00.627757 1648648380
Buy: Price(crypto='ADA', currency='USD', amount=1.19)
Sell: Price(crypto='ADA', currency='USD', amount=1.17)
Spot: Price(crypto='ADA', currency='USD', amount=1.1791)
```
