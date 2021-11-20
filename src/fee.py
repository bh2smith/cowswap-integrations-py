import requests

from . import domains


class Fee:
    def __init__(self, sell_token, buy_token, sell_amount, kind, buy_amount):
        self.sell_token = sell_token
        self.buy_token = buy_token
        self.sell_amount = sell_amount
        self.buy_amount = buy_amount
        self.kind = kind
        self.base_url = domains.base_url

    def get_fee(self) -> "uint256":
        url = "{}fee?sellToken={}&buyToken={}&amount={}&kind={}".format(
            self.base_url,
            self.sell_token,
            self.buy_token,
            self.buy_amount,
            self.kind
        )

        request_fee = requests.get(url)
        return int(request_fee.json().get("amount", 0))
