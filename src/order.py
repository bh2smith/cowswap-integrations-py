import json
import time

import requests
from eip712.messages import EIP712Message
from hexbytes import HexBytes
from web3.auto import w3
from eth_account import Account

from . import domains
from .encoding import BytesJSONEncoder


class Order(EIP712Message):
    _name_: "string" = domains.name
    _version_: "string" = domains.version
    _chainId_: "uint256" = domains.chain_id
    _verifyingContract_: "address" = domains.verifying_contract
    _trader_: "address" = domains.private_key
    _quoteId_: "uint32" = 0
    _appDataRaw_: "string" = "{\"appCode\": \"cowswap-integrations-py\"}"

    sellToken: "address" = "0x0000000000000000000000000000000000000000"
    buyToken: "address" = "0x0000000000000000000000000000000000000000"
    receiver: "address" = "0x0000000000000000000000000000000000000000"
    sellAmount: "uint256" = 0
    buyAmount: "uint256" = 0
    validTo: "uint32" = int(int(time.time()) + 240)
    appData: "bytes32" = HexBytes(
        "0x000000000000000000000000000000000000000000000000000000000000ca1f")
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
    
    def swithSellTokenBalance(self, sellTokenBalance):
        self.sellTokenBalance = sellTokenBalance
        return self
    
    def withBuyTokenBalance(self, buyTokenBalance):
        self.buyTokenBalance = buyTokenBalance
        return self

    def __sign(self):
        sig = w3.eth.account.sign_message(
            self.signable_message,
            private_key=domains.private_key
        )
        return sig.signature.hex()

    def json(self):
        order = {}
        order['sellToken'] = self.sellToken
        order['buyToken'] = self.buyToken
        order['receiver'] = self.receiver
        order['sellAmount'] = str(self.sellAmount)
        order['buyAmount'] = str(self.buyAmount)
        order['validTo'] = self.validTo
        order['feeAmount'] = str(self.feeAmount)
        order['kind'] = self.kind
        order['partiallyFillable'] = self.partiallyFillable
        order['sellTokenBalance'] = self.sellTokenBalance
        order['buyTokenBalance'] = self.buyTokenBalance
        order['signingScheme'] = "eip712"
        order['signature'] = self.__sign()
        order['from'] = Account.from_key(self._trader_).address
        order['quoteId'] = self._quoteId_
        order['appData'] = self._appDataRaw_
        return order

    def post(self):
        r = requests.post(domains.base_url + "orders", data=json.dumps(self.json(), cls=BytesJSONEncoder))
        return r.json()

    def quote(self):
        order_data = self.json();
        if self.kind == "buy" or self.buyAmount > 0:
            order_data['buyAmountAfterFee'] = str(self.sellAmount)
        else:
            order_data['sellAmountBeforeFee'] = str(self.sellAmount)
        print(f"Quote Request: {json.dumps(order_data, cls=BytesJSONEncoder)}")
        r = requests.post(domains.base_url + "quote", data=json.dumps(order_data, cls=BytesJSONEncoder))
        print(f"Quote Response: {r.json()}")
        if r.status_code != 200:
          raise "Quote Failed"

        self.feeAmount = int(r.json()['quote']['feeAmount'])
        self.buyAmount = int(r.json()['quote']['buyAmount'])
        self.sellAmount = int(r.json()['quote']['sellAmount'])
        self.kind = r.json()['quote']['kind']
        self.appData = HexBytes(r.json()['quote']['appDataHash'])
        self._quoteId_ = r.json()['id']
        return self

    def slippage(self, slippageBps):
        if self.kind == "sell":
            self.buyAmount = self.buyAmount * (10000 - slippageBps) // 10000
            print(f"Buy Amount after slippage: {self.buyAmount}")
        else:
            self.sellAmount = self.sellAmount * (10000 + slippageBps) // 10000
            print(f"Sell Amount after slippage: {self.sellAmount}")
        return self
