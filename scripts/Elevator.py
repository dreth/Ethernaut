from scripts.helper.context import *
from scripts.helper.account import _from, acc
from brownie import Elevator, Building

##########################################
# This elevator won't let you reach the top of your building. Right?
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    elevator = load_challenge(ContractObject=Elevator, instance_key='elevator')
    building = Building.deploy(elevator.address, _from)

    # go to floor the top floor which has to be different to the
    # initializing value of a uint, which is 0
    building.goToTopFloor(_from)

    # then check if we're at the top
    top_assertion = elevator.top() == True
    print(f'We are at the top floor: {top_assertion}')

    return top_assertion

def main():
    solve_challenge()
