import unittest
import json

from eth_account import Account

from src.martins_script import Order as OldOrder
from src.order import Order


class OldOrderTests(unittest.TestCase):
    def test_opposite_kind(self):
        buy_order = OldOrder(sell_token="TokenA", buy_token="TokenB", receiver="",
                             sell_amount=1, buy_amount=2, valid_to=0, fee_amount=1,
                             kind="buy")
        self.assertEqual(buy_order.opposite_kind(), "sell")
        sell_order = OldOrder(sell_token="TokenA", buy_token="TokenB", receiver="",
                              sell_amount=1, buy_amount=2, valid_to=0, fee_amount=1,
                              kind="sell")
        self.assertEqual(sell_order.opposite_kind(), "buy")


class OrderTests(unittest.TestCase):
    def test_sign(self):
        sell_token = "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83"
        buy_token = "0x4ecaba5870353805a9f068101a40e0f32ed605c6"
        sell_amount = 1000000
        buy_amount = 1000000
        kind = "buy"
        fee_amount = 887

        pk = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
        receiver = Account.from_key(pk).address
        # Must specify validTo because it fixes the order parameters and
        # makes the signature deterministic.
        order = Order(sell_token, buy_token, receiver, sell_amount, buy_amount, fee_amount, kind,
                      validTo=1639052668)
        required_signature = "0x547b936d1aac1b0153776887ee23a92097d3988c433b0d9642014c9861e07f8f3e16cbc7d1c2d42d3f3b32b332f2aafc86daace610a0a5968b93733c79c87a1a1b"
        self.assertEqual(order.sign, required_signature)
        expected_order = json.load("""{
            "sellToken": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83", 
            "buyToken": "0x4ecaba5870353805a9f068101a40e0f32ed605c6", 
            "receiver": "0xD2Cc479Be0512301D0B19C3C0A9300bAA1E03758", 
            "sellAmount": "1000000", 
            "buyAmount": "1000000", 
            "validTo": 1639052668, 
            "appData": "0x000000000000000000000000000000000000000000000000000000000000ca1f", 
            "feeAmount": "887",
            "kind": "buy", 
            "partiallyFillable": false, 
            "sellTokenBalance": "erc20", 
            "buyTokenBalance": "erc20", 
            "signature": "0x547b936d1aac1b0153776887ee23a92097d3988c433b0d9642014c9861e07f8f3e16cbc7d1c2d42d3f3b32b332f2aafc86daace610a0a5968b93733c79c87a1a1b", 
            "signingScheme": "eip712"}""")
        self.assertEqual(order.set_json, expected_order)


if __name__ == '__main__':
    unittest.main()
