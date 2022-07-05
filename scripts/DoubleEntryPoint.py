from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import DoubleEntryPoint, DetectionBot, Forta, CryptoVault, history

##########################################
# Your job is to implement a detection bot and register it in the Forta contract. The bot's implementation will need to raise correct alerts to prevent potential attacks or bug exploits.
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    # not locally
    if not locally:
        dep = load_challenge(ContractObject=DoubleEntryPoint, instance_key='doubleentrypoint')
    else:
        dep = deploy_locally(ContractObject=DoubleEntryPoint, from_account=_from)

    # get cryptovault address
    cryptovault_address = dep.cryptoVault()

    # instantiate the cryptovault contract
    cryptovault = CryptoVault.at(cryptovault_address)

    # deploy and set the bot
    forta = Forta.at(dep.forta())
    bot = DetectionBot.deploy(cryptovault_address, forta.address, _from)
    forta.setDetectionBot(bot.address, _from)

    # get the legacy token contract address
    legacytoken = dep.delegatedFrom()

    # sweep the tokens
    try:
        cryptovault.sweepToken(legacytoken, _from | {'allow_revert':True})
    except:
        pass

    # transaction was reverted by the contract
    revert_msg_assertion = history[-1].revert_msg == 'Alert has been triggered, reverting'
    print(f"The transaction triggered the forta alert: {revert_msg_assertion}")

    return revert_msg_assertion

def main():
    solve_challenge()
