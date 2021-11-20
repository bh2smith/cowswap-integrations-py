from src.fee import Fee
from src.order import Order


def cow_swap():
    # fill variables below and fill network, public address and private key in .env
    sell_token = "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83"
    buy_token = "0x4ecaba5870353805a9f068101a40e0f32ed605c6"
    sell_amount = 1000000
    buy_amount = 1000000
    kind = "buy"

    fee = Fee(sell_token, buy_token, sell_amount, kind, buy_amount)
    fee_amount = fee.get_fee()
    order = Order(sell_token, buy_token, sell_amount, buy_amount, fee_amount, kind)
    print(order.post_order())


if __name__ == "__main__":
    cow_swap()
