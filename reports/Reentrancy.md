# Reentrancy

## Objectives

The goal of this level is for you to steal all the funds from the contract.

## Solution

the Reentrance contract seems to only expect non-contract addresses to interact with it. When calling `donate()` through a contract and donating an amount of ETH, we can then call `withdraw()` and have another call to `withdraw()` as a fallback function where we attempt to withdraw the same amount that was sent during the donation. This allows our contract to withdraw once again from the Reentrance contract before it can actually update its balance, leading to a net loss of funds equal to the amount that was donated _per transaction_. If the contract had a larger amount of funds, we could basically repeat this same transaction as long as it is gas-efficient to do so and eventually deplete the contract's funds.

## How I did it

1. Code and deploy a contract (at: `0xe2F7Cc547AE5F07C06DA81837877F0056Fb23B6a`) with 4 functions, one to donate, another one to withdraw and a last one being a fallback function that can receive funds `receive()`. The fallback function will call the `withdraw()` method from the Reentrance contract. Additionally, a 4th function that withdraws the attacking contract's funds back to the deployer.

2.We repeat the donate --> withdraw process until the contract has been drained. In this case, the contract had a total of 0.001 ETH (1e15 wei) in it, so it can be done in a single loop. Despite this, I still wanted to use a while loop for illustrative/learning purposes.

```python
while reentrancy.balance() > 0:
    reentrancyattack.donate({'value': 1e15} | _from)
    reentrancyattack.withdraw(1e15, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x8382be6a150e53084ef3dddd1eddb2947f67f06ef78462762bee0da5e4706c92

Block explorer: https://rinkeby.etherscan.io/tx/0xfd45877eea70901376b99b2bee25d924696adbe6cf3fa88aae2d9a58f579884e

3. Recover the funds from the attacker contract and send them to the deployer (owner, me)
   
```python
reentrancyattack.withdrawAttackerContractFunds(_from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xbe8c59fba36d2911e1a82c38ad9b6b1790688af717a195cdc7de4270eeb71526


4. Check if the contract has indeed been drained.

```python
balance_assertion = reentrancy.balance() == 0
print(f"The contract's balance is {reentrancy.balance()}, The contract is {'drained' if balance_assertion else 'not drained'}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0xe704da1a83ed2a3ecf4b72876222c46dc65e9fe72b2ab5d4e1be2262698a73b8
