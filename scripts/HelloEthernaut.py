from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import Instance

# solve the challenge
def solve_challenge():
    # load challenge
    HelloEthernaut = load_challenge(ContractObject=Instance, instance_key='hello')

    # run methods
    print(HelloEthernaut.info1(_from))
    print(HelloEthernaut.info2("hello", _from))
    print(HelloEthernaut.infoNum(_from))
    print(HelloEthernaut.info42(_from))
    print(HelloEthernaut.theMethodName(_from))
    print(HelloEthernaut.method7123949(_from))

    # get password
    password = HelloEthernaut.password()

    # authenticate
    HelloEthernaut.authenticate(password, _from)

    # determine if done
    cleared = HelloEthernaut.getCleared(_from)
    print(cleared)

    return cleared
    
def main():
    solve_challenge()
