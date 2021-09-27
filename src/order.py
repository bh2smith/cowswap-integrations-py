import time
import eip712_structs
from typing import Set, Optional

import requests
from eip712_structs import Address, Boolean, Bytes, String, Uint, EIP712Struct
from eth_account.messages import encode_defunct
from web3.auto import w3

# TODO - all the global declarations here should become environment vars passed in
#  as arguments at runtime. Specifically,
#  `network`/`chain_id`, `private_key`, `base_url`, `stable_coins`, `verifyingContract`
network = "xdai"
if network == "mainnet":
    base_url = "https://protocol-mainnet.gnosis.io/api/v1/"
    private_key = "XXXX"
    public_address = "0xE2A4dFC3Cab6dCdb198C83066B93110D62d95F09"
    domain = eip712_structs.make_domain(
        name='Gnosis Protocol',
        version='v2',
        chainId='1',
        verifyingContract="0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
    )
else:
    base_url = "https://protocol-xdai.gnosis.io/api/v1/"
    private_key = "XXXX"
    public_address = "0x89145F922BB420453bCd8a7Be87dA830C0941f22"
    domain = eip712_structs.make_domain(
        name='Gnosis Protocol',
        version='v2',
        chainId='100',
        verifyingContract="0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
    )

ETH = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

WETH_ADDRESS = {
    "mainnet": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "xdai": "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d"
}

WETH = WETH_ADDRESS[network]

stable_coins = {
    "0xddafbb505ad214d7b80b1f830fccc89b60fb7a83": 6,  # USDC
    "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d": 18,  # wxDAI
    "0x4ecaba5870353805a9f068101a40e0f32ed605c6": 6  # USDT
}


class Order(EIP712Struct):
    # TODO - not sure I'm fond of this object field declaration...
    #  what ever happened to __init__?
    sell_token = Address()
    buy_token = Address()
    receiver = Address()
    sell_amount = Uint(256)
    buy_amount = Uint(256)
    valid_to = Uint(32)
    app_data = Bytes(32)
    fee_amount = Uint(256)
    kind = String()
    partially_fillable = Boolean()
    sell_token_balance = String()
    buy_token_balance = String()

    def __init__(
            self,
            sell_token: Address,
            buy_token: Address,
            receiver: Address,
            sell_amount: Uint,
            buy_amount: Uint,
            valid_to: Uint(32),
            fee_amount: Uint,
            kind: String
    ):
        # Is there some nicer way of doing this? Seems so repetitive.
        # never allow native eth to be a token always use WETH.
        self.sell_token = sell_token if sell_token != ETH else WETH
        self.buy_token = buy_token if buy_token != ETH else WETH
        self.receiver = receiver
        self.sell_amount = sell_amount
        self.buy_amount = buy_amount
        self.fee_amount = fee_amount
        self.kind = kind
        self.valid_to = valid_to
        # These all essentially don't matter.
        self.app_data = "0x8008135000000000000000000000000000000000000000000000000000000000"
        self.partially_fillable = False
        self.sell_token_balance = "erc20"
        self.buy_token_balance = "erc20"

    def set_fee(self):
        self.fee_amount = self.get_fee()

    def is_profitable(self) -> bool:
        # Types don't line up here, but python doesn't seem care.
        buy_value = self.buy_amount / pow(10, stable_coins[self.buy_token])
        sell_value = self.sell_amount / pow(10, stable_coins[self.sell_token])
        return buy_value > sell_value

    def tokens(self) -> Set[Address]:
        return {self.buy_token, self.sell_token}

    def opposite_kind(self) -> String:
        if self.kind == "sell":
            return "buy"
        return "sell"

    def get_fee(self) -> Optional[int]:
        if self.kind in {"buy", "sell"}:
            url = "{0}fee?sellToken={1}&buyToken={2}&amount={3}&kind={4}".format(
                base_url, self.sell_token, self.buy_token, str(self.sell_amount),
                self.kind)
            fee_response = requests.get(url).json()
        else:
            # TODO - log something here.
            return
        return int(fee_response["amount"]) or 0

    def to_json(self, signed_message, public_key):
        # TODO - make this less ugly
        # self.__dict__ + extend by missing bits
        json_str = '''{
          "sellToken": "''' + str(self["sellToken"]) + '''",
          "buyToken": "''' + str(self["buyToken"]) + '''",
          "receiver": "''' + str(self["receiver"]) + '''",
          "sellAmount": "''' + str(self["sellAmount"]) + '''",
          "buyAmount": "''' + str(self["buyAmount"]) + '''",
          "validTo": ''' + str(self["validTo"]) + ''',
          "appData": "''' + str(self["appData"].hex()) + '''",
          "feeAmount": "''' + str(self["feeAmount"]) + '''",
          "kind": "''' + str(self["kind"]) + '''",
          "partiallyFillable": ''' + str(self["partiallyFillable"]).lower() + ''',
          "signature": "''' + str(signed_message.signature.hex()) + '''",
          "signingScheme": "ethsign",
          "sellTokenBalance": "''' + str(self["sellTokenBalance"]) + '''",
          "buyTokenBalance": "''' + str(self["buyTokenBalance"]) + '''",
          "from": "''' + public_key + '''"
        }'''
        return json.loads(json_str)

    def place_order(self):
        self.fee_amount = self.get_fee()
        order_bytes = self.signable_bytes(domain)
        order_hash = w3.keccak(order_bytes)
        message = encode_defunct(primitive=order_hash)
        signed_message = w3.eth.account.sign_message(message, private_key=private_key)
        # Build Json out of Order + signed_message.signature.hex() + public_address
        order_json = self.to_json(signed_message, public_address)
        r = requests.post(base_url + "orders", json=order_json)
        # TODO - log status code.

    def counter_order(self):
        # TODO - stop accessing fields by string keys.
        res = Order(
            sell_token=self.buy_token,
            buy_token=self.sell_token,
            receiver=public_address,
            sell_amount=self.buy_amount,
            buy_amount=self.sell_amount,
            # 2 minutes in the future.
            valid_to=int(time.time()) + 120,
            kind=self.opposite_kind(),
        )
        res.fee_amount = res.get_fee()
        # TODO - could make method set_fee which updates field directly.
        return res
