from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import Shop, Buyer

##########################################
# Сan you get the item from the shop for less than the price asked?
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        shop = load_challenge(ContractObject=Shop, instance_key='shop')
    else:
        shop = deploy_locally(ContractObject=Shop, from_account=_from)
    
    # deploy Buyer contract
    buyer = Buyer.deploy(shop.address, _from)

    # call buy() function in shop contract
    buyer.shop(_from)

    # check the sold price
    price_assertion = shop.price() < 100
    print(f"The selling price is below 100: {price_assertion}")

    return price_assertion    

def main():
    solve_challenge()
