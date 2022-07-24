# Ethernaut solutions

In this repo I will write all the solutions to the [Ethernaut CTF](https://ethernaut.openzeppelin.com/). I solved the challenges locally using brownie. Then did it on chain on brownie on the rinkeby test network through the Infura API. To fork rinkeby I used the Alchemy API.

## My local environment setup

1. Install relevant libraries

```
pip install eth-brownie rlp eth-utils eth_abi
```

2. Get a new instance of every challenge by going on the ethernaut site and clicking on `Get new instance` for every chapter.

3. Copy the address for every single one of my instances and save them in a script within `/scripts/helper` called `ethernaut_addresses.py`. All are in a dictionary for easier identification of each contract/instance. The script also contains a dictionary called `EthernautContractAddresses` with all the addresses for the contracts as they were deployed when I started the challenge (7th June, 2022). If you want to use my setup, you'll need to change the `EthernautInstances` and add your instances there, the `EthernautContractAddresses` variable can be deleted. 

If you want to use the factory contracts (contracts that create your instance of each challenge), then modify the values in `EthernautContractAddresses`. I have not included the factory contracts because I didn't really need them, for my purposes, everything could be tested by just running scripts in a local fork of the rinkeby test network, if you want to do this, you'll have to change my setup somewhat significantly.

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

If you want to play around in your local development blockchain, then just pass `locally=True` to `solve_challenge()` under `main()` and make sure to run the script passing `development` under the network flag, like this:  `brownie run ScriptName --network development`, where `ScriptName` is the name of the script you're running. 


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

## Helper scripts

Under `/scripts/helper` I have included a few convenience scripts that I imported in every single script (as needed), some were _always_ needed, like the Ethernaut instance addresses or my account import. 

The helper scripts are:

- `account.py`: imports the account to be used to solve the challenges, the actual account that I use to deploy/submit my instances
- `ethernaut_addresses.py`: contains all the instance and contract addresses
- `utils.py`: contains some basic functions that I use in each script. I always do a full import of everything in this script because here I defined the `load_challenge()` function which loads the instance of each challenge.
- `web3.py`: contains an instance of web3 which I use for whatever utility from the web3.py library that I might need

## Templates

I have also added a small template for scripts, reports and attacker/interaction contracts I might need. They're under the `template` folder of `reports`, `contracts` and `scripts`.

## My solutions

All my solutions are layed out in [this article](https://dac.ac/blog/ethernaut_solutions/) on my blog, however, you can also see the solutions here on github in the markdown documents under `/reports`. You can view whichever you want by clicking on its name:

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
