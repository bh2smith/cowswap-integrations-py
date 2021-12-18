import unittest
import json

from eth_account import Account

from martins_script import Order as OldOrder
from order import Order


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

        # Must specify validTo because it fixes the order parameters and
        # makes the signature deterministic.
        order = Order(sell_token, buy_token, sell_amount, buy_amount, fee_amount, kind,
                      validTo=1639052668)
        required_signature = "0xa2d34aff599383dd6a86826e3caf087077350567daaad3173c54d945bef3c6a865a02a831af7fc67d07d844bd120a83fbe1ea2f60c8af157e86c100c6693e85f1b"
        self.assertEqual(order.sign(), required_signature)
        expected_order = json.loads('''{
            "sellToken": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83", 
            "buyToken": "0x4ecaba5870353805a9f068101a40e0f32ed605c6", 
            "receiver": "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1", 
            "sellAmount": "1000000", 
            "buyAmount": "1000000", 
            "validTo": 1639052668, 
            "appData": "0x000000000000000000000000000000000000000000000000000000000000ca1f", 
            "feeAmount": "887",
            "kind": "buy", 
            "partiallyFillable": false, 
            "sellTokenBalance": "erc20", 
            "buyTokenBalance": "erc20", 
            "signature": "0xa2d34aff599383dd6a86826e3caf087077350567daaad3173c54d945bef3c6a865a02a831af7fc67d07d844bd120a83fbe1ea2f60c8af157e86c100c6693e85f1b", 
            "signingScheme": "eip712"}''')
        self.assertEqual(json.loads(order.set_json()), expected_order)


if __name__ == '__main__':
    unittest.main()
