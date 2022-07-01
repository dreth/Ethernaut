from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import DoubleEntryPoint

##########################################
# Your job is to implement a detection bot and register it in the Forta contract. The bot's implementation will need to raise correct alerts to prevent potential attacks or bug exploits.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        dep = load_challenge(ContractObject=DoubleEntryPoint, instance_key='doubleentrypoint')
    else:
        dep = deploy_locally(ContractObject=DoubleEntryPoint, from_account=_from)
    
    # get cryptovault address
    cryptovault_address = dep.cryptoVault()

    

    


def main():
    solve_challenge()
