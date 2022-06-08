from web3 import Web3
from web3.middleware import geth_poa_middleware
import os

web3 = Web3(Web3.HTTPProvider(f"https://eth-rinkeby.alchemyapi.io/v2/{os.environ['ALCHEMY_API_KEY_RINKEBY']}"))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
