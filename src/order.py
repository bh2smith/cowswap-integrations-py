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

    sellToken: "address"
    buyToken: "address"
    receiver: "address" = Account.from_key(domains.private_key).address
    sellAmount: "uint256"
    buyAmount: "uint256"
    validTo: "uint32" = int(int(time.time()) + 240)
    appData: "bytes32" = HexBytes(
        "0x000000000000000000000000000000000000000000000000000000000000ca1f")
    feeAmount: "uint256"
    kind: "string"
    partiallyFillable: "bool" = False
    sellTokenBalance: "string" = "erc20"
    buyTokenBalance: "string" = "erc20"

    def sign(self, private_key: str):
        sig = w3.eth.account.sign_message(
            self.signable_message,
            private_key=private_key
        )
        return str(sig.signature.hex())

    def set_json(self):
        order = self.body_data['message']
        order['signature'] = self.sign()
        order['signingScheme'] = "eip712"
        # TODO - We shouldn't have to do this! maybe a method called "garnish"
        order['sellAmount'] = str(self.sellAmount)
        order['buyAmount'] = str(self.buyAmount)
        order['feeAmount'] = str(self.feeAmount)
        return json.dumps(order, indent=4, cls=BytesJSONEncoder)

    def post_order(self):
        r = requests.post(domains.base_url + "orders", data=self.set_json())
        return r.text
