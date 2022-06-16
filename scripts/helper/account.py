from brownie import accounts
import os

# account to use
acc = accounts.load('acc', password=os.environ['ACCOUNT_PASSWORD'])
_from = {'from':acc}
