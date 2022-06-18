from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import Recovery

##########################################
# This level will be completed if you can recover (or remove) the 0.001 ether from the lost contract address.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        recovery = load_challenge(ContractObject=Recovery, instance_key='recovery')
    else:
        recovery = deploy_locally(ContractObject=Recovery, from_account=_from)

def main():
    solve_challenge()
