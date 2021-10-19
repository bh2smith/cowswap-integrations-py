from eip712_structs import EIP712Struct, Address, Boolean, Bytes, String, Uint
import requests
import json
from eip712_structs import make_domain
from web3.auto import w3
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
import time

class Fee: 
    def __init__(self, sellToken, buyToken, sellAmount, kind):
        self.sellToken = sellToken
        self.buyToken = buyToken
        self.sellAmount = sellAmount
        self.kind = kind
    
    def setFee(self):
        self.base_url = base_url
        url = "{}fee?sellToken={}&buyToken={}&amount={}&kind={}".format(
            self.base_url, 
            self.sellToken, 
            self.buyToken,
            self.sellAmount,
            self.kind
            )
        requestFee = requests.get(url)
        feeAmount = int(requestFee.json()["amount"])
        return feeAmount

class Signature:
    def __init__(self, privateKey, name, version, chainId, verifyingContract):
        self.privateKey = privateKey
        self.name = name
        self.version = version
        self.chainId = chainId
        self.verifyingContract = verifyingContract     
    
    def getSig(self):
        my_bytes = self.signable_bytes(self.getDomain(name, version, chainId, verifyingContract))
        hash = w3.keccak(my_bytes)
        message = encode_defunct(primitive=hash)
        signed_message = w3.eth.account.sign_message(message, private_key=privateKey)
        return signed_message.signature.hex()

    def getDomain(self, name, version, chainId, verifyingContract):
        return make_domain(name=name, version=version, chainId=chainId, verifyingContract=verifyingContract)

class Order(Fee, Signature, EIP712Struct):
    def __init__(self, sellToken, buyToken, sellAmount, kind, receiver, buyAmount, validTo, appData, partiallyFillable, sellTokenBalance, buyTokenBalance, signingScheme, orders):
        self.sellToken: Address() = sellToken
        self.buyToken: Address() = buyToken
        self.sellAmount: Uint(256) = sellAmount
        self.kind: String() = kind
        self.receiver: Address() = receiver
        self.buyAmount: Uint(256) = buyAmount
        self.validTo: Uint(32) = validTo
        self.appData: Bytes(32) = appData
        self.feeAmount: Uint(256) = str(Fee.setFee(self, base_url))
        self.partiallyFillable: Boolean() = partiallyFillable
        self.signature = Signature.getSig(self)
        self.signingScheme = signingScheme
        self.sellTokenBalance: String() = sellTokenBalance
        self.buyTokenBalance: String() = buyTokenBalance 
    
    def toJson(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)
                
    def submitOrder(self, base_url):
        self.base_url = base_url
        return requests.post("{}orders".format(self.base_url), json=self.toJson())

#part you have to fill yourself:
sellToken = "0xddafbb505ad214d7b80b1f830fccc89b60fb7a83"    
buyToken = "0x4ecaba5870353805a9f068101a40e0f32ed605c6"     
sellAmount = "123456"      
receiver = "XXXX"     #your own public address
buyAmount = "123456"                         
privateKey = "XXXX" #your private key here without 0x

#part you have to change if you want to use other network then xDAI
base_url = "https://protocol-xdai.gnosis.io/api/v1/"       
version = "v2"                                                  
chainId = "100"  
verifyingContract = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"

#dont change these:
name = "Gnosis Protocol"                                                                
kind = "buy"                                                
validTo = int(time.time()) + 120                     
appData = "0x0000000000000000000000000000000000000000000000000000000000000ccc" 
partiallyFillable = False                                
sellTokenBalance = "erc20"                                 
buyTokenBalance = "erc20"                                   
signingScheme = "ethsign"

CowSwapOrder = Order(sellToken, buyToken, sellAmount, kind, receiver, buyAmount, validTo, appData, partiallyFillable, sellTokenBalance, buyTokenBalance, signingScheme, orders)
print(CowSwapOrder.submitOrder(base_url))



