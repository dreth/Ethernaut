# Ethernaut challenge (brownie)

Hi, in this repo I will learn how to use brownie by doing the [Ethernaut challenge from OpenZeppelin.](https://ethernaut.openzeppelin.com/)

## Forking rinkeby using brownie

Searching online I found how to do this in [this ethereum stackexchange question](https://ethereum.stackexchange.com/questions/113294/does-anyone-know-how-to-fork-a-chain-at-a-particular-block-on-brownie). 1000x thanks to Patrick Collins for his great video tutorials, courses and this ethereum stakexchange answer.

Add a fork of rinkeby to the list of ganache-cli networks with its corresponding RPC:

```
brownie networks add development rinkeby-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-rinkeby.alchemyapi.io/v2/$ALCHEMY_API_KEY_RINKEBY@10801707 accounts=10 mnemonic=brownie port=8545
```

