from dataclasses import dataclass
from datetime import datetime, timedelta
import sqlite3
import requests


@dataclass
class Price:
    crypto: str
    currency: str
    amount: float


@dataclass
class CoinbasePriceRow:
    timestamp: datetime
    crypto: str
    currency: str
    buy_price: float
    sell_price: float
    spot_price: float


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


@dataclass
class CoinbasePriceTable:
    db_loc: str

    def save(self, row: CoinbasePriceRow) -> None:
        conn = sqlite3.connect(self.db_loc)
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS "coinbase_prices" (
                "date"	INTEGER NOT NULL,
                "crypto"	TEXT NOT NULL,
                "currency"	TEXT NOT NULL,
                "buy_price"	REAL NOT NULL,
                "sell_price"	REAL NOT NULL,
                "spot_price"	REAL,
                PRIMARY KEY("date","crypto","currency")
            )"""
        )
        fields = (
            int(
                row.timestamp.timestamp()
            ),  # sqlite does not support datetime columns at this time
            row.crypto,
            row.currency,
            row.buy_price,
            row.sell_price,
            row.spot_price,
        )
        cur.execute(f"INSERT INTO coinbase_prices VALUES (?, ?, ?, ?, ?, ?)", fields)
        conn.commit()
        conn.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a DB of Coinbase prices.")
    parser.add_argument("currency", help="The currency of the price.")
    parser.add_argument("crypto", help="The cryptocurrency coin code.")
    parser.add_argument("--db", default="prices.sqlite", help="Database location.")

    args = parser.parse_args()

    # round time down to nearest minute
    now = datetime.now()
    now -= timedelta(seconds=now.second)

    client = CoinbasePrices()
    print("Time:", now, int(now.timestamp()))
    buy = client.get_buy_price(args.crypto, args.currency)
    print("Buy:", buy)
    sell = client.get_sell_price(args.crypto, args.currency)
    print("Sell:", sell)
    spot = client.get_spot_price(args.crypto, args.currency)
    print("Spot:", spot)

    row = CoinbasePriceRow(
        now,
        buy.crypto,
        buy.currency,
        buy_price=buy.amount,
        sell_price=sell.amount,
        spot_price=spot.amount,
    )
    table = CoinbasePriceTable(args.db)
    table.save(row)
