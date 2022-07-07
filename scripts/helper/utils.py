from scripts.helper.ethernaut_addresses import *
import rlp
from eth_utils import keccak, to_checksum_address, to_bytes
from brownie import accounts

# test locally
def deploy_locally(ContractObject, from_account, constructor_params=[]):
    # prepare the params that pass to the constructor as a string
    # that looks like "param1, param2, param3," etc
    if constructor_params:
        params = ''
        for param in constructor_params:
            # if the param is an address, it needs to pass as a string
            if param[0:2] == '0x':
                params += f'"{param}",'
            # otherwise, it's fine passing as it is
            else:
                params += f'{param},'
        contract = eval(f'ContractObject.deploy({params} from_account)')
    else:
        contract = eval(f'ContractObject.deploy(from_account)')
    return contract

# redefine _from and acc for local use
def define_from_acc():
    return {'from':accounts[0]}, accounts[0]

# load challenge from instances
def load_challenge(ContractObject, instance_key):
    return ContractObject.at(EthernautInstances[instance_key])

# compute address of a given contract to be deployed from
# the deployer address + nonce, as stated in the Section 7 
# of the Ethereum yellowpaper for contracts created using CREATE
def mk_contract_address(sender: str, nonce: int) -> str:
    """Create a contract address using eth-utils.
    # Modified from Mikko Ohtamaa's original answer which was later
    # edited by Utgarda
    # Obtained from https://ethereum.stackexchange.com/questions/760/how-is-the-address-of-an-ethereum-contract-computed
    """
    sender_bytes = to_bytes(hexstr=sender)
    raw = rlp.encode([sender_bytes, nonce])
    h = keccak(raw)
    address_bytes = h[12:]
    return to_checksum_address(address_bytes)
