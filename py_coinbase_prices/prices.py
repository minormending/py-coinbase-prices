from dataclasses import dataclass
from datetime import datetime, timedelta
from locale import currency
import sqlite3
from time import time
import requests


@dataclass
class Price:
    crypto: str
    currency: str
    amount: float


class CoinbasePrices:
    def __init__(self) -> None:
        self.prices_api = "https://api.coinbase.com/v2/prices"

    def get_buy_price(self, crypto: str, currency: str) -> Price:
        url: str = f"{self.prices_api}/{crypto}-{currency}/buy"
        resp = requests.get(url)
        result = resp.json().get("data")
        return Price(
            crypto=result.get("base"),
            currency=result.get("currency"),
            amount=float(result.get("amount")),
        )

    def get_sell_price(self, crypto: str, currency: str) -> Price:
        url: str = f"{self.prices_api}/{crypto}-{currency}/sell"
        resp = requests.get(url)
        result = resp.json().get("data")
        return Price(
            crypto=result.get("base"),
            currency=result.get("currency"),
            amount=float(result.get("amount")),
        )

    def get_spot_price(self, crypto: str, currency: str) -> Price:
        url: str = f"{self.prices_api}/{crypto}-{currency}/spot"
        resp = requests.get(url)
        result = resp.json().get("data")
        return Price(
            crypto=result.get("base"),
            currency=result.get("currency"),
            amount=float(result.get("amount")),
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a DB of Coinbase prices.")
    parser.add_argument("crypto", help="The cryptocurrency coin code.")
    parser.add_argument("currency", help="The currency of the price.")

    args = parser.parse_args()

    client = CoinbasePrices()
    now = datetime.now()
    now -= timedelta(seconds=now.second)
    print("Time:", now, int(now.timestamp()))
    buy = client.get_buy_price(args.crypto, args.currency)
    print("Buy:", buy)
    sell = client.get_sell_price(args.crypto, args.currency)
    print("Sell:", sell)
    spot = client.get_spot_price(args.crypto, args.currency)
    print("Spot:", spot)


    conn = sqlite3.connect('prices.sqlite')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO coinbase_prices VALUES ({int(now.timestamp())}, '{buy.crypto}', '{buy.currency}', {buy.amount}, {sell.amount}, {spot.amount})")
    conn.commit()
    conn.close()