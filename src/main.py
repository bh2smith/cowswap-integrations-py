from Fee import Fee
from order import Order



def CowSwap():
    #fill variables below and fill network in Domains.py
    sellToken = "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83"
    buyToken = "0x4ecaba5870353805a9f068101a40e0f32ed605c6"
    sellAmount = 1000000
    buyAmount = 1000000
    kind = "buy"

    fee = Fee(sellToken, buyToken, sellAmount, kind, buyAmount)
    feeAmount = fee.get_fee()  
    order = Order(sellToken, buyToken, sellAmount, buyAmount, feeAmount, kind)
    print(order.post_order())

if __name__ == "__main__": CowSwap()
