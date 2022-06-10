from web3 import Web3
import os

web3 = Web3(Web3.HTTPProvider(f"https://eth-rinkeby.alchemyapi.io/v2/{os.environ['ALCHEMY_API_KEY_RINKEBY']}"))
