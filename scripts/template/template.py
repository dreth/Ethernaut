from scripts.context import *
from scripts.account import _from, acc
from brownie import ContractName

##########################################
# Goal of the exercise
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    contract_name = load_challenge(contract_name=ContractName, instance_key='contract_name')

def main():
    solve_challenge()
