import json
import time
from eip712.messages import EIP712Message  # pylint: disable=import-error

import requests
from requests import HTTPError
from hexbytes import HexBytes
from web3.auto import w3
from eth_account import Account

from src import domains
from src.encoding import BytesJSONEncoder


class Order(EIP712Message):
    _name_: "string" = domains.name
    _version_: "string" = domains.version
    _chainId_: "uint256" = domains.chain_id
    _verifyingContract_: "address" = domains.verifying_contract
    _trader_: "address" = domains.private_key
    _quoteId_: "uint32" = 0
    _appDataRaw_: "string" = '{"appCode": "cowswap-integrations-py"}'

    sellToken: "address" = "0x0000000000000000000000000000000000000000"
    buyToken: "address" = "0x0000000000000000000000000000000000000000"
    receiver: "address" = "0x0000000000000000000000000000000000000000"
    sellAmount: "uint256" = 0
    buyAmount: "uint256" = 0
    validTo: "uint32" = int(int(time.time()) + 240)
    appData: "bytes32" = HexBytes(
        "0x000000000000000000000000000000000000000000000000000000000000ca1f"
    )
    feeAmount: "uint256" = 0
    kind: "string" = "sell"
    partiallyFillable: "bool" = False
    sellTokenBalance: "string" = "erc20"
    buyTokenBalance: "string" = "erc20"

    def withSellToken(self, sellToken):
        self.sellToken = sellToken
        return self

    def withBuyToken(self, buyToken):
        self.buyToken = buyToken
        return self

    def withSellAmount(self, sellAmount):
        self.sellAmount = sellAmount
        return self

    def withBuyAmount(self, buyAmount):
        self.buyAmount = buyAmount
        return self

    def withFrom(self, private_key):
        self._trader_ = private_key
        return self

    def withReceiver(self, receiver):
        self.receiver = receiver
        return self

    def withValidTo(self, validTo):
        self.validTo = validTo
        return self

    def withAppData(self, appData):
        self.appData = appData
        return self

    def withFeeAmount(self, feeAmount):
        self.feeAmount = feeAmount
        return self

    def withKind(self, kind):
        self.kind = kind
        return self

    def withPartiallyFillable(self, partiallyFillable):
        self.partiallyFillable = partiallyFillable
        return self

    def withSellTokenBalance(self, sellTokenBalance):
        self.sellTokenBalance = sellTokenBalance
        return self

    def withBuyTokenBalance(self, buyTokenBalance):
        self.buyTokenBalance = buyTokenBalance
        return self

    def __sign(self):
        sig = w3.eth.account.sign_message(
            self.signable_message, private_key=domains.private_key
        )
        return sig.signature.hex()

    def json(self):
        order = {
            "sellToken": self.sellToken,
            "buyToken": self.buyToken,
            "receiver": self.receiver,
            "sellAmount": str(self.sellAmount),
            "buyAmount": str(self.buyAmount),
            "validTo": self.validTo,
            "feeAmount": str(self.feeAmount),
            "kind": self.kind,
            "partiallyFillable": self.partiallyFillable,
            "sellTokenBalance": self.sellTokenBalance,
            "buyTokenBalance": self.buyTokenBalance,
            "signingScheme": "eip712",
            "signature": self.__sign(),
            "from": Account().from_key(private_key=self._trader_).address,
            "quoteId": self._quoteId_,
            "appData": self._appDataRaw_,
        }
        return order

    def post(self):
        r = requests.post(
            domains.base_url + "orders",
            data=json.dumps(self.json(), cls=BytesJSONEncoder),
            timeout=10,
        )
        return r.json()

    def quote(self):
        order_data = self.json()
        if self.kind == "buy" or self.buyAmount > 0:
            order_data["buyAmountAfterFee"] = str(self.sellAmount)
        else:
            order_data["sellAmountBeforeFee"] = str(self.sellAmount)
        print(f"Quote Request: {json.dumps(order_data, cls=BytesJSONEncoder)}")
        r = requests.post(
            domains.base_url + "quote",
            data=json.dumps(order_data, cls=BytesJSONEncoder),
            timeout=10,
        )
        print(f"Quote Response: {r.json()}")
        if r.status_code != 200:
            raise HTTPError(f"Quote Failed with status code {r.status_code}")

        self.feeAmount = int(r.json()["quote"]["feeAmount"])
        self.buyAmount = int(r.json()["quote"]["buyAmount"])
        self.sellAmount = int(r.json()["quote"]["sellAmount"])
        self.kind = r.json()["quote"]["kind"]
        self.appData = HexBytes(r.json()["quote"]["appDataHash"])
        self._quoteId_ = r.json()["id"]
        return self

    def slippage(self, slippageBps):
        if self.kind == "sell":
            self.buyAmount = self.buyAmount * (10000 - slippageBps) // 10000
            print(f"Buy Amount after slippage: {self.buyAmount}")
        else:
            self.sellAmount = self.sellAmount * (10000 + slippageBps) // 10000
            print(f"Sell Amount after slippage: {self.sellAmount}")
        return self
