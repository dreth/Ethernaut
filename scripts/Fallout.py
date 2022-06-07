from scripts.context import *
from scripts.account import _from, acc
from brownie import Fallout

##########################################
# You will beat this level if

# 1. you claim ownership of the contract
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    fallback = load_challenge(contract_name=Fallout, instance_key='fallback')

    

    
def main():
    solve_challenge()
