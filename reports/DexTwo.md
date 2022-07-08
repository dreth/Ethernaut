# DexTwo

## Objectives

You need to drain all balances of token1 and token2 from the DexTwo contract to succeed in this level.

## Solution

The DexTwo problem suffers from a different problem to the Dex problem. In this case, there is no require statement checking whether the two token contract addresses being swapped actually match the two token contract addresses for which the pool is designed. As correctly defined in the Dex contract, this line is missing:

```js
require((from == token1 && to == token2) || (from == token2 && to == token1), "Invalid tokens");
```

As a result of this, we can code another ERC20 token contract of which we mint the entire supply to our wallet and with just a few of these we can drain both sides of the pool as follows:

1. Create a new ERC20 token and mint the entire supply to our wallet. As defined in the SwappableTokenTwo contract or otherwise.

2. Send a few of those tokens to the DexTwo contract.

3. Approve the DexTwo contract for spending our new token.

4. Transfer some of the new tokens to the contract, so that the contract can compute the internal ratio in it of the tokens using the same flawed `getSwapAmount()` function.

5. Perform 2 swaps, one to drain the balance of Token 1 and another one to drain the balance of Token 2 by swapping of our Token 3 (the new token) for them.

6. Because we can control the internal ratio and we can perform swaps with zero checks of whether the address is the correct one or not, the pool can be easily drained.

## How I did it

Exactly as described in [solution](#solution).

1. Code and deploy a new ERC20 token (at: `0xc27a45c6D84F6AB7aAFECFB82d0853064e288261`)

```python
dextwoattack = DexTwoAttack.deploy('token3', 'TK3', '10000000000000', _from)
```

2. Approve the DexTwo contract spending limit for our new token

```python
dextwoattack.approve(dextwo.address, 2**256 - 1, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x8a25d4bcb33d461f536192aecc1a3137ba17293341ce2235c958c5b3d675e1bf

3. Transfer some of the new tokens to the DexTwo contract

```python
dextwoattack.transfer(dextwo.address, 10, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xd2a9c745602a8b5f87117939d22133e877657ff030e6eeb0258260bdd47a072c

4. Perform both swaps, one to drain the balance of Token 1 and the other one to drain the balance of Token 2

Block explorer: https://rinkeby.etherscan.io/tx/0x9a8a5397aed89c3fb0570c293f3465af37ebc658c5a1e241891774e749bb083c

Block explorer: https://rinkeby.etherscan.io/tx/0x8f1434586d9cbfb6774c8be95c3e8a2b538c3c09ee0a3b6978daff585898bded

5. Check whether we have successfully drained the pools or not

```python
# check the balances
balanceTK1 = dextwo.balanceOf(tk1, dextwo.address)
balanceTK2 = dextwo.balanceOf(tk2, dextwo.address)
print(f"The pool balances are: TK1: {balanceTK1}, TK2: {balanceTK2}")

# the pools have been drained
balance_assertion = balanceTK1 == 0 and balanceTK2 == 0
print(f"The pools have been drained: {balance_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x2ad048ca0de3d4f6c1bdd78862d202dad7a7d68bd9ed87fc0ea98a511efd205c
