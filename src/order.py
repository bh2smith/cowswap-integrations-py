from eip712.messages import EIP712Message
import time
from hexbytes import HexBytes
from web3.auto import w3
import Domains
import json
import requests
from JSONEncoder import BytesJSONEncoder

class Order(EIP712Message):
    _name_: "string" = Domains.name
    _version_: "string" = Domains.version
    _chainId_: "uint256" = Domains.chainId
    _verifyingContract_: "address" = Domains.verifyingContract

    sellToken: "address"
    buyToken: "address"
    receiver: "address" = Domains.public_address1
    sellAmount: "uint256"
    buyAmount: "uint256"
    validTo: "uint32" = int(int(time.time()) + 240)
    appData: "bytes32" = HexBytes("0x0000000000000000000000000000000000000000000000000000000000000ccc")
    feeAmount: "uint256" 
    kind: "string"
    partiallyFillable: "bool" = False
    sellTokenBalance: "string" = "erc20"
    buyTokenBalance: "string" = "erc20"

    def get_sig(self):
        sig = w3.eth.account.sign_message(self.signable_message, private_key=Domains.privatekey1)
        return str(sig.signature.hex())

    def set_JSON(self):
        orders = self.body_data['message']
        orders['signature'] = self.get_sig()
        orders['signingScheme'] = "eip712"
        orders['sellAmount'] = str(self.sellAmount)
        orders['buyAmount'] = str(self.buyAmount)
        orders['feeAmount'] = str(self.feeAmount)
        return json.dumps(orders, indent=4, cls=BytesJSONEncoder)

    def post_order(self):
        r = requests.post(Domains.base_url + "orders", data=self.set_JSON())
        return r.text
