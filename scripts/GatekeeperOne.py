from scripts.context import *
from scripts.account import _from, acc
from brownie import GatekeeperOne

##########################################
# Make it past the gatekeeper and register as an entrant to pass this level.
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    gatekeeper = load_challenge(contract_name=GatekeeperOne, instance_key='gatekeeper')

def main():
    solve_challenge()
