import unittest

from src.martins_script import Order


class OrderTests(unittest.TestCase):
    def test_opposite_kind(self):
        buy_order = Order(sell_token="TokenA", buy_token="TokenB", receiver="",
                          sell_amount=1, buy_amount=2, valid_to=0, fee_amount=1,
                          kind="buy")
        self.assertEqual(buy_order.opposite_kind(), "sell")
        sell_order = Order(sell_token="TokenA", buy_token="TokenB", receiver="",
                           sell_amount=1, buy_amount=2, valid_to=0, fee_amount=1,
                           kind="sell")
        self.assertEqual(sell_order.opposite_kind(), "buy")


if __name__ == '__main__':
    unittest.main()
