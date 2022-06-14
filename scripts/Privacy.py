from scripts.context import *
from scripts.account import _from, acc
from scripts.web3 import web3
from brownie import Privacy

##########################################
# Unlock this contract to beat the level.
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    privacy = load_challenge(contract_name=Privacy, instance_key='privacy')

    # get bytes32 object in storage position 0x5
    # that's where the third element of data is located (solidity is 0-index as nature was supposed to be)
    data_2 = web3.toBytes(hexstr=web3.eth.getStorageAt(privacy.address, '0x5').hex())[0:16].hex()

    # call unlock function passing in data_2
    privacy.unlock(data_2, _from)

    # check if it's unlocked
    locked_assertion = privacy.locked() == False
    print(f"The contract is unlocked: {locked_assertion}")

    return locked_assertion

def main():
    solve_challenge()
