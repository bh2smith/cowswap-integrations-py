from dotenv import load_dotenv
import os

load_dotenv()

network = "xdai"

if(network == "xdai"):
#xdai
    base_url = "https://protocol-xdai.gnosis.io/api/v1/"
    name = "Gnosis Protocol"
    version = "v2"
    chainId = 100
    verifyingContract = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
    public_address1 = os.getenv("PUBLIC_ADDRESS")
    privatekey1 = os.getenv("PRIVATE_KEY")
    botaddress = "0x89145F922BB420453bCd8a7Be87dA830C0941f22"
else:
    #ethereum
    base_url = "https://protocol-mainnet.gnosis.io/api/v1/"
    name = "Gnosis Protocol"
    version = "v2"
    chainId = 1
    verifyingContract = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"

