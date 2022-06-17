# NaughtCoin

## Objectives

Complete this level by getting your token balance to 0.

## Solution

The ERC20 implementation, which the NaughtCoin contract inherits from, includes functionality for externally owned accounts or contracts to transfer funds out of a specific address given that that address has approved the externally owned account or contract to transfer funds out of it.

This can be done by first calling the function `approve()` from the account holding the NaughtCoins and then `transferFrom()` to transfer the tokens out of the account from the EOA or contract that was approved initially.

In two steps:

1. Call `approve()` as follows:

```cs
approve(Account2Address, Account1Balance)
```

2. Call `transferFrom()` as follows:

```cs
transferFrom(Account1Address, Account2Address, Account1Balance)
```

Where:

* `Account1Address`: Address of account holding the NaughtCoins
  
* `Account1Balance`: Amount of NaughtCoins in `Account1Address`, can be obtained by calling `balanceOf(Account1Address)`
  
* `Account2Address`: Address of account which will be allowed to move the tokens out of `Account1Address`. 

In this case it's also possible to send the tokens to the burn address `0x0000000000000000000000000000000000000000`.

## How I did it

1. Call `approve()` to allow a second account to move the tokens out of the account holding them. Make sure to approve *at least* the entire balance of tokens in the wallet in order to drain it.

```python
balance_in_wallet = naughtcoin.balanceOf(acc.address)
naughtcoin.approve(acc2.address, balance_in_wallet, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xdd23e9d864d89405610ec5211eca4a6ebc0a9962a7f6a837163f658b53ec97bc

2. Call `transferFrom()` to move the full token balance out of account 1 (`acc`) and into account 2 (`acc2`).

```python
naughtcoin.transferFrom(acc.address, acc2.address, balance_in_wallet, _from2)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xc906a92a4e70cd69b24d33d6b4af67ae061ed86d40f7d26f3fd36bb174bcbbd2

3. Check that the balance is indeed zero

```python
balance_assertion = naughtcoin.balanceOf(acc.address) == 0
print(f"The account balance has been drained: {balance_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0xee3cf83fb11b43d97f5667e8c4bb3a242821d527284a15ff4265d565ddee3eab
