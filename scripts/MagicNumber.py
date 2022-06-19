from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import MagicNum

##########################################
# To solve this level, you only need to provide the Ethernaut with a Solver, a contract that responds to whatIsTheMeaningOfLife() with the right number.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        magicnumber = load_challenge(ContractObject=MagicNum, instance_key='magicnumber')
    else:
        magicnumber = deploy_locally(ContractObject=MagicNum, from_account=_from)
    
    # set solver
    magicnumber.setSolver('0x678a4e09ec08d8fd32abc0f4e3e28469fe8b6e80', _from)

    return True

def main():
    solve_challenge()
