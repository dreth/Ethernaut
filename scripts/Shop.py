from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import Shop

##########################################
# Сan you get the item from the shop for less than the price asked?
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        shop = load_challenge(ContractObject=Shop, instance_key='shop')
    else:
        shop = deploy_locally(ContractObject=Shop, from_account=_from)
    
    
    


def main():
    solve_challenge()
