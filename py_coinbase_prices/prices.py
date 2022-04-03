from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
from requests import Session, Response
import sqlite3


@dataclass
class Price:
    crypto: str
    currency: str
    amount: float


@dataclass
class Error:
    id: str
    message: str


@dataclass
class CoinbasePriceRow:
    timestamp: datetime
    crypto: str
    currency: str
    buy_price: float
    sell_price: float
    spot_price: float


class InvalidCryptoCurrencyError(Exception):
    pass


class InvalidFiatCurrencyError(Exception):
    pass


class CoinbasePrices:
    def __init__(self) -> None:
        self.prices_api = "https://api.coinbase.com/v2/prices"
        self.session = Session()

    def _check_response_for_error(self, resp: Response) -> None:
        if resp.status_code == 404 or resp.status_code == 400:
            if errors := resp.json().get("errors"):
                error = Error(**errors[0])
                if error.id.lower() == "not_found":
                    raise InvalidCryptoCurrencyError(error.message)
                if error.id.lower() == "invalid_request":
                    raise InvalidFiatCurrencyError(error.message)

    def _get_price_obj(self, resp: Response) -> Price:
        self._check_response_for_error(resp)

        result = resp.json().get("data")
        return Price(
            crypto=result.get("base"),
            currency=result.get("currency"),
            amount=float(result.get("amount")),
        )

    def get_buy_price(self, crypto: str, currency: str) -> Price:
        url: str = f"{self.prices_api}/{crypto}-{currency}/buy"
        resp = self.session.get(url)
        return self._get_price_obj(resp)

    def get_sell_price(self, crypto: str, currency: str) -> Price:
        url: str = f"{self.prices_api}/{crypto}-{currency}/sell"
        resp = self.session.get(url)
        return self._get_price_obj(resp)

    def get_spot_price(self, crypto: str, currency: str) -> Price:
        url: str = f"{self.prices_api}/{crypto}-{currency}/spot"
        resp = self.session.get(url)
        return self._get_price_obj(resp)


@dataclass
class CoinbasePriceTable:
    db_loc: str

    def save(self, rows: List[CoinbasePriceRow]) -> None:
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
        for row in rows:
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
            cur.execute(
                f"INSERT OR REPLACE INTO coinbase_prices VALUES (?, ?, ?, ?, ?, ?)",
                fields,
            )
        conn.commit()
        conn.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a DB of Coinbase prices.")
    parser.add_argument("currency", help="The currency of the price.")
    parser.add_argument("cryptos", nargs="+", help="The cryptocurrency coin code.")
    parser.add_argument("--db", default="prices.sqlite", help="Database location.")

    args = parser.parse_args()

    client = CoinbasePrices()
    table = CoinbasePriceTable(args.db)

    rows: List[CoinbasePriceRow] = []
    for crypto in args.cryptos:
        now = datetime.now()
        now -= timedelta(seconds=now.second)  # round time down to nearest minute

        try:
            buy = client.get_buy_price(crypto, args.currency)
            sell = client.get_sell_price(crypto, args.currency)
            spot = client.get_spot_price(crypto, args.currency)
            print("\nTime:", now, int(now.timestamp()))
            print("Buy:", buy)
            print("Sell:", sell)
            print("Spot:", spot)
        except InvalidCryptoCurrencyError as ex:
            print(f"Error: Crypto currency `{crypto}` is not supported by Coinbase!")
            continue
        except InvalidFiatCurrencyError as ex:
            print(
                f"Error: Fiat currency `{args.currency}` is not supported by Coinbase!"
            )
            exit(1)  # none of the crypto currencies will succeed

        rows.append(
            CoinbasePriceRow(
                now,
                buy.crypto,
                buy.currency,
                buy_price=buy.amount,
                sell_price=sell.amount,
                spot_price=spot.amount,
            )
        )

    table.save(rows)
