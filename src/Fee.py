import requests
import json
import Domains


class Fee: 
    def __init__(self, sellToken, buyToken, sellAmount, kind, buyAmount):
        self.sellToken = sellToken
        self.buyToken = buyToken
        self.sellAmount = sellAmount
        self.kind = kind
        self.buyAmount = buyAmount
        self.base_url = Domains.base_url

    def get_fee(self):
        if self.kind == "buy":
            url = "{}fee?sellToken={}&buyToken={}&amount={}&kind={}".format(
                self.base_url, 
                self.sellToken, 
                self.buyToken,
                self.buyAmount,
                self.kind
            )
        else:
            url = "{}fee?sellToken={}&buyToken={}&amount={}&kind={}".format(
                self.base_url, 
                self.sellToken, 
                self.buyToken,
                self.sellAmount,
                self.kind
            )
        requestFee = requests.get(url)
        if "amount" in requestFee.json().keys():
            feeAmount = int(requestFee.json()["amount"])
        else:
            feeAmount = 0
        return feeAmount

       