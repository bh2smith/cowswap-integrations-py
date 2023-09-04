import unittest
import json

from src.order import Order


class OrderTests(unittest.TestCase):
    def test_sign(self):
        # Must specify validTo because it fixes the order parameters and
        # makes the signature deterministic.
        order = (
            Order()
            .withSellToken("0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83")
            .withBuyToken("0x4ecaba5870353805a9f068101a40e0f32ed605c6")
            .withSellAmount(1000000)
            .withBuyAmount(1000000)
            .withFeeAmount(887)
            .withKind("buy")
            .withValidTo(1639052668)
        )

        self.assertEqual(
            order.json().get("signature"),
            "0x39a13c31ac9327396b75b9f537fabbd8e738d84f03f76b607e5ecae31bbf19416e98846a1953492d0dcbb5037140f9e0e894b13affeb0985a368b5ee55c1c3df1b",
        )
        expected_order = json.loads(
            """{
            "sellToken": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83", 
            "buyToken": "0x4ecaba5870353805a9f068101a40e0f32ed605c6", 
            "from": "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",
            "receiver": "0x0000000000000000000000000000000000000000", 
            "sellAmount": "1000000", 
            "buyAmount": "1000000", 
            "validTo": 1639052668, 
            "appData": {"appCode": "cowswap-integrations-py"}, 
            "feeAmount": "887",
            "quoteId": 0,
            "kind": "buy", 
            "partiallyFillable": false, 
            "sellTokenBalance": "erc20", 
            "buyTokenBalance": "erc20", 
            "signature": "0x39a13c31ac9327396b75b9f537fabbd8e738d84f03f76b607e5ecae31bbf19416e98846a1953492d0dcbb5037140f9e0e894b13affeb0985a368b5ee55c1c3df1b", 
            "signingScheme": "eip712"}"""
        )
        self.assertEqual(order.json(), expected_order)


if __name__ == "__main__":
    unittest.main()
