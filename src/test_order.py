import unittest

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
        fee_amount = 1

        pk = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
        receiver = Account.from_key(pk).address
        # Must specify validTom because it fixes the order parameters and
        # makes the signature deterministic.
        order = Order(sell_token, buy_token, sell_amount, buy_amount, fee_amount, kind,
                      receiver, validTo=1234)
        self.assertEqual(order.signature, "")
        order.sign("0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d")
        self.assertEqual(
            "0x17f0bf89c33f5a8ebb750904783421ca127ac59c2680672a69aebc08cd0b644562b19c0a97e34a69e26345459cfccce8276410b933eeded485e2d552ccfaa5211b",
            order.signature
        )


# expected = json.load("""
# {
#     "sellToken": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
#     "buyToken": "0x4ecaba5870353805a9f068101a40e0f32ed605c6",
#     "receiver": "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",
#     "sellAmount": "1000000",
#     "buyAmount": "1000000",
#     "validTo": 1638052668,
#     "appData": "0x000000000000000000000000000000000000000000000000000000000000ca1f",
#     "feeAmount": "885",
#     "kind": "buy",
#     "partiallyFillable": false,
#     "sellTokenBalance": "erc20",
#     "buyTokenBalance": "erc20",
#     "signingScheme": "eip712",
#     "signature": "0xf659927f204c1da68526cf209c1523167a2aeb1cbbc2854318d2e7dfb9e8270e29153778afdb605b079af1e5f3cb575ff65b4afdf6546d657df60acf71a1aa5a1c"
# }""")

if __name__ == '__main__':
    unittest.main()
