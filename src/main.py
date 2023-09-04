from src.order import Order


def cow_swap():
    # fill variables below and fill network, public address and private key in .env
    uid = (
        Order()
        .withSellAmount(100000000000000000)
        .withSellToken("0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d")
        .withBuyToken("0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83")
        .quote()
        .slippage(50)
        .post()
    )
    print(f"Successfully placed order: https://explorer.cow.fi/orders/{uid}")


if __name__ == "__main__":
    cow_swap()
