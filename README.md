# Ethernaut solutions

In this repo I will write all the solutions to the [Ethernaut CTF](https://ethernaut.openzeppelin.com/). I solved the challenges locally using brownie. Then did it on chain through brownie as well using the rinkeby network through the Infura api.

## My local environment setup

1. Install relevant libraries

```
pip install eth-brownie rlp eth-utils eth_abi
```

2. Get a new instance of every single challenge by going on the ethernaut site and clicking on `Get new instance` for every chapter.

3. Copy the address for every single one of my instances and save them in a script within `/scripts` called `context.py`. All are in a dictionary for easier identification of each contract/instance. The script also contains a dictionary called `EthernautContractAddresses` with all the addresses for the contracts as they were deployed when I started the challenge (7th June, 2022). If you want to use my setup, you'll need to change the `EthernautInstances` and add your instances there, the `EthernautContractAddresses` variable can be deleted.

4. Add an account to brownie using the CLI: 

```
brownie accounts new <account name>
```

Then paste the private key of the account used to deploy the instances in step 1. For safety reasons, do not use an account that has funds on mainnet or any other network that isn't a testnet.

5. Once the account is added, go to the `account.py` helper file, where you can define the account object to then be imported into the scripts. I used two accounts, so I defined two, the main one `acc` and `acc2`. In my case, `acc` also coincides with the account creating and submitting the Ethernaut instances. I do this because after testing locally, I simply changed networks to rinkeby in order to submit the transactions as they were submitted in the forked rinkeby (as described in step 9)

6. Do each challenge in a script within the `/scripts` folder and use the following template (also as `template.py` in `/scripts/template/`) for each script:

```python
from scripts.helper.utils import *
from scripts.helper.account import _from, acc
from brownie import ContractName

##########################################
# Goal of the exercise
#########################################

# solve the challenge
def solve_challenge(locally=False):
    # load challenge
    if not locally:
        contract_name = load_challenge(ContractObject=ContractName, instance_key='contract_name')
    else:
        contract_name = deploy_locally(ContractObject=ContractName, from_account=_from)
    
def main():
    solve_challenge()
```

Modify the variables at the start of `solve_challenge()` accordingly:

* `ContractName`: name of the contract object, as defined in the solidity scripts

* `'contract_name'`: key of the contract address as present in `/scripts/helper/ethernaut_addresses.py`


7. Run everything in a forked rinkeby testnet local network, first add the network. Optionally use a specific block:

```
brownie networks add development rinkeby-fork cmd=ganache host=http://127.0.0.1 fork=https://eth-rinkeby.alchemyapi.io/v2/$ALCHEMY_API_KEY_RINKEBY@Block accounts=10 mnemonic=brownie port=8545
```

You can either use the infura or alchemy APIs, I personally used alchemy. I set the `ALCHEMY_API_KEY_RINKEBY` environment variable on my machine, but you can do so in the `.env` file by modifying the `.env.template` file and removing the `.template` part of the filename.

8. Then run whatever script you want to run using this local forked network:

```
brownie run <script> --network rinkeby-fork
```

9. **Once you're ready to submit your instance**, in order to make the submission, just change what network you run the script in to rinkeby _after_ you have confirmed it works in your forked rinkeby instance. After each tx confirms, you can submit your instance.

```
brownie run <script> --network rinkeby
```

**NOTE: [The Rinkeby test network is deprecated](https://ethereum.org/en/developers/docs/networks/#rinkeby) in favor of the Sepolia/Görli testnet. There's a high chance that after Rinkeby has been deprecated, OpenZeppelin will deploy Ethernaut in the Sepolia or Görli testnet.** As a result of this, you should keep in mind that steps 7-9 of my setup will be on a different testnet.

## My solutions

For my solution reports/writeups are in the markdown documents under `/reports`. You can view whichever you want by clicking on its name:

1. [HelloEthernaut](https://github.com/dreth/Ethernaut/blob/main/reports/HelloEthernaut.md)
2. [Fallback](https://github.com/dreth/Ethernaut/blob/main/reports/Fallback.md)
3. [Coin Flip](https://github.com/dreth/Ethernaut/blob/main/reports/CoinFlip.md)
4. [Telephone](https://github.com/dreth/Ethernaut/blob/main/reports/Telephone.md)
5. [Token](https://github.com/dreth/Ethernaut/blob/main/reports/Token.md)
6. [Delegation](https://github.com/dreth/Ethernaut/blob/main/reports/Delegation.md)
7. [Force](https://github.com/dreth/Ethernaut/blob/main/reports/Force.md)
8. [Vault](https://github.com/dreth/Ethernaut/blob/main/reports/Vault.md)
9. [King](https://github.com/dreth/Ethernaut/blob/main/reports/King.md)
10. [Re-entrancy](https://github.com/dreth/Ethernaut/blob/main/reports/Re-entrancy.md)
11. [Elevator](https://github.com/dreth/Ethernaut/blob/main/reports/Elevator.md)
12. [Privacy](https://github.com/dreth/Ethernaut/blob/main/reports/Privacy.md)
13. [Gatekeeper One](https://github.com/dreth/Ethernaut/blob/main/reports/GatekeeperOne.md)
14. [Gatekeeper Two](https://github.com/dreth/Ethernaut/blob/main/reports/GatekeeperTwo.md)
15. [Naught Coin](https://github.com/dreth/Ethernaut/blob/main/reports/NaughtCoin.md)
16. [Preservation](https://github.com/dreth/Ethernaut/blob/main/reports/Preservation.md)
17. [Recovery](https://github.com/dreth/Ethernaut/blob/main/reports/Recovery.md)
18. [Magic Number](https://github.com/dreth/Ethernaut/blob/main/reports/MagicNumber.md)
19. [Alien Codex](https://github.com/dreth/Ethernaut/blob/main/reports/AlienCodex.md)
20. [Denial](https://github.com/dreth/Ethernaut/blob/main/reports/Denial.md)
21. [Shop](https://github.com/dreth/Ethernaut/blob/main/reports/Shop.md)
22. [Dex](https://github.com/dreth/Ethernaut/blob/main/reports/Dex.md)
23. [Dex Two](https://github.com/dreth/Ethernaut/blob/main/reports/DexTwo.md)
24. [PuzzleWallet](https://github.com/dreth/Ethernaut/blob/main/reports/PuzzleWallet.md)
25. [Motorbike](https://github.com/dreth/Ethernaut/blob/main/reports/Motorbike.md)
26. [DoubleEntryPoint](https://github.com/dreth/Ethernaut/blob/main/reports/DoubleEntryPoint.md)
