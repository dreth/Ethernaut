from scripts.helper.context import *
from scripts.helper.account import _from, acc
from brownie import GatekeeperTwo, GatekeeperTwoAttack

##########################################
# Register as an entrant to pass this level.
#########################################

# test locally
def deploy_locally(ContractObject, from_account, constructor_params={}):
    return ContractObject.deploy(from_account, **constructor_params)

# solve the challenge
def solve_challenge(locally=False):
    if not locally:
        # load challenge
        gatekeeper = load_challenge(ContractObject=GatekeeperTwo, instance_key='gatekeeper2')
    else:
        gatekeeper = deploy_locally(ContractObject=GatekeeperTwo, from_account=_from)
    
    # deploy attacker contract
    gk2attack = GatekeeperTwoAttack.deploy(gatekeeper.address, _from)

    # check if we're entrant
    entrant_assertion = gatekeeper.entrant() == acc.address
    print(f"Address is entrant: {entrant_assertion}")

    return entrant_assertion


def main():
    solve_challenge()
