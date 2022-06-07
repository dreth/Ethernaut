# Ethernaut solutions

In this repo I will write all the solutions to the [Ethernaut CTF](https://ethernaut.openzeppelin.com/). I solved the challenges locally using brownie. Then did it on chain through brownie as well using the rinkeby network through the Infura api.

## My local environment setup

1. Get a new instance of every single challenge by going on the ethernaut site and clicking on `Get new instance` for every chapter.

2. Copy the address for every single one of my instances and save them in a script within `/scripts` called `context.py`. All are in a dictionary for easier identification of each contract/instance. The script also contains a dictionary called `EthernautContractAddresses` with all the addresses for the contracts as they were deployed when I started the challenge (7th June, 2022). If you want to use my setup, you'll need to change the `EthernautInstances` and add your instances there, the `EthernautContractAddresses` variable can be deleted.

3. Add an account to brownie using the CLI: 

```
brownie accounts new <account name>
```

Then paste the private key of the account used to deploy the instances in step 1. For safety reasons, do not use an account that has funds on mainnet or any other network that isn't a testnet.

4. Do each challenge in a script within the `/scripts` folder and use the following template for each script:

```python
from scripts.context import *
from scripts.account import _from, acc
from brownie import <contract_to_import>

##########################################
# how is the level beat? 
# copy paste it from the ethernaut site
#########################################

# solve the challenge
def solve_challenge():
    # load challenge
    <lowercase_contract_name> = load_challenge(contract_name=<contract_to_import>, instance_key='<contract_instance_key_from_EthernautInstances>')

def main():
    solve_challenge()
```

Modify the variables at the start of `solve_challenge()` accordingly:

* `<lowercase_contract_name>`: name of the contract you're working on in lowercase

* `<contract_to_import>`: name of the contract object you're working with, this should be imported from `brownie` as well

* `<contract_instance_key_from_EthernautInstances>`: the key you used on the `EthernautInstances` dictionary keys to refer to the address of the contract's instance


5. Run everything in a forked rinkeby testnet local network, first add the network. Optionally use a specific block:

```
brownie networks add development rinkeby-fork cmd=ganache host=http://127.0.0.1 fork=https://eth-rinkeby.alchemyapi.io/v2/$ALCHEMY_API_KEY_RINKEBY@Block accounts=10 mnemonic=brownie port=8545
```

You can either use the infura or alchemy APIs, I personally used alchemy. I set the `ALCHEMY_API_KEY_RINKEBY` environment variable on my machine, but you can do so in the `.env` file by modifying the `.env.template` file and removing the `.template` part of the filename.

6. Then run whatever script you want to run using this local forked network:

```
brownie run <script> --network rinkeby-fork
```
