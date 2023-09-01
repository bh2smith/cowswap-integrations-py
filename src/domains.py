import os

from dotenv import load_dotenv
load_dotenv()

private_key = os.getenv("PRIVATE_KEY")
network = os.getenv("NETWORK")

base_url = f"https://api.cow.fi/{network}/api/v1/"
name = "Gnosis Protocol"
version = "v2"
verifying_contract = "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"

if network == 'xdai':
    chain_id = 100
elif network == 'mainnet':
    chain_id = 1
else:
    chain_id = None
