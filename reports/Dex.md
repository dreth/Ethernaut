# Dex

## Objectives

The goal of this level is for you to hack the basic DEX contract below and steal the funds by price manipulation.

## Solution

First we have to approve both tokens for transfer, which we can conveniently do with the `approve()` function in the Dex contract. Then we take advantage of the poor way to compute the price used by the contract. 

The ratio used to compute the price of each asset is as follows:

$$getSwapPrice(T_n, T_k, A) = A * \frac{balanceOf(T_n, Dex)}{balanceOf(T_k, Dex)}$$

Where:

* $getSwapPrice(T_n, T_k, A)$ is the function to compute the price of the asset
* $A$ is the amount of the token to be traded
* $T$ is the contract address of a given token, subindexes $n$, $k$ represent integers referring to the name of the tokens, in this case we have Token 1 and Token 2, though the `getSwapPrice` function can be called 
* $Dex$ is the address of the Dex contract

This ratio computation is severely flawed and can very easily be used to attack the contract. We can see that by simply using the 10 tokens we're given to perform swaps, the ratio becomes completely unbalanced, as we are simply relying on the available supply on the assets stored in the contract.

***

To illustrate the imbalance each swap creates, let's simulate the first 3 scenarios:

#### First swap

With:

* $A_{T_1} = 10$
* $balanceOf(T_1, Dex) = 100$
* $balanceOf(T_2, Dex) = 100$:

Then:

$$T_1 \rightarrow T_2 \approx 10$$

After each swap, the balances will change, as we are putting units of $T_1$ in the pool and taking out units of $T_2$ and vice versa.

#### Second swap

With:

* $A_{T_2} = 10$
* $balanceOf(T_1, Dex) = 110$
* $balanceOf(T_2, Dex) = 90$:

Then:

$$T_2 \rightarrow T_1 \approx 12$$

Here we already see that by putting back the same 10 $T_2$ tokens we put in, we can now take out 12 $T_1$ tokens. This is because the internal price in the pool is now unbalanced. 

#### Third swap

With 

* $A_{T_1} = 12$
* $balanceOf(T_1, Dex) = 98$
* $balanceOf(T_2, Dex) = 100$:

Then:

$$T_2 \rightarrow T_1 \approx 12$$

This last swap illustrates that of the total pool balance, we have effectively 'stolen' 2% of the $T_1$ balance. Executing the swap several additional times, creates enough asset imbalance so that there's no longer any assets in one side of the pool. If we continue though, we would drain both liquidity sides.

#### Balances at each swap

| Swap | Balance $T_1$ | Balance $T_2$ | Floor of $getSwapPrice(T_n, T_k, 10)$ |
|------|---------------|---------------|---------------------------------------|
| 0    | 100           | 100           | 10                                    |
| 1    | 110           | 90            | 12                                    |
| 2    | 98            | 100           | 10                                    |
| 3    | 110           | 88            | 12                                    |
| 4    | 83            | 110           | 13                                    |
| 5    | 110           | 75            | 14                                    |
| 6    | 59            | 110           | 18                                    |
| 7    | 110           | 15            | 7                                     |
| 8    | 0             | 30            | Inf                                   |

Even though I used the floor of the price, solidity will still apparently internally use decimals prior to casting to integer. As a result of this, swap 8 will cause the pool to be drained, as $7.\bar{3} * 15 = 110$.

## How I did it

1. First call the `approve()` function in the Dex contract:

```python
# use the convenient approve method in dex
dex.approve(dex.address, 2*256 - 1, _from)
```

0x3a7d2248b69cd0cc34fa41e32c8b27ee9d20c9c59129d7c68c5530b29e70845f

2. Then I perform enough swaps until the pool is drained, which I do inside an infinite while loop that breaks when the condition that at least one of the balances of a token in the Dex is drained. The following if-else statement performs each swap, all the swaps except the last one using as the amount my balance of each token per swap (alternates through the boolean `c` which is used to index this dictionary `switch = {True: {1: tk1, 2: tk2}, False: {1: tk2, 2: tk1}}`):

```python
# perform action
if (my_bal < dex_bal1(c)):
    dex.swap(switch[c][1], switch[c][2], my_bal, _from)
else:
    dex.swap(switch[c][1], switch[c][2], dex_bal1(c), _from)

# check if we are done
if dex_bal1(c) == 0 or dex_bal2(c) == 0:
    break
```

Table with the swaps and tx hashes:

| Swap | Balance $T_1$ | Balance $T_2$ | Tx hash of each one of the swaps                                   |
|------|---------------|---------------|--------------------------------------------------------------------|
| 0    | 100           | 100           | [0xded5a80cd702d0f330f0acdda86248b0622a9c05d59a3fb7d7ef8abd1e2fdc12](https://rinkeby.etherscan.io/tx/0xded5a80cd702d0f330f0acdda86248b0622a9c05d59a3fb7d7ef8abd1e2fdc12) |
| 1    | 110           | 90            | [0xa1b979e946ea9e75ec484309773d11f9c1dba0e5a7894a421a3fdfb3401a2428](https://rinkeby.etherscan.io/tx/0xa1b979e946ea9e75ec484309773d11f9c1dba0e5a7894a421a3fdfb3401a2428) |
| 2    | 98            | 100           | [0xdfccc83437533c5a142583426a858f7cdf1bee830548523222f353c86775a31e](https://rinkeby.etherscan.io/tx/0xdfccc83437533c5a142583426a858f7cdf1bee830548523222f353c86775a31e) |
| 3    | 110           | 88            | [0x60703c7c78c142f8ad9e9279b7a4a1478d5d48715220d8775f9dfebe5343b7e1](https://rinkeby.etherscan.io/tx/0x60703c7c78c142f8ad9e9279b7a4a1478d5d48715220d8775f9dfebe5343b7e1) |
| 4    | 83            | 110           | [0xe08e68d42b49de0aecef4df9a94e6fd3ad93389155735a896f347e20e84593df](https://rinkeby.etherscan.io/tx/0xe08e68d42b49de0aecef4df9a94e6fd3ad93389155735a896f347e20e84593df) |
| 5    | 110           | 75            | [0x5be83195ec1369e34cc05c7b097e15611ef9e8a8d4a00f8a3e97f829e7ff148c](https://rinkeby.etherscan.io/tx/0x5be83195ec1369e34cc05c7b097e15611ef9e8a8d4a00f8a3e97f829e7ff148c) |
| 6    | 59            | 110           | [0x44b5e1ff748c05acdf87128d7b68af188cb76e47a226744568c246e36b352773](https://rinkeby.etherscan.io/tx/0x44b5e1ff748c05acdf87128d7b68af188cb76e47a226744568c246e36b352773) |
| 7    | 110           | 15            | [0xaf0676991ff5583ac68e13197df00b7e0bfa1796f7769519721c8bff8e72ced8](https://rinkeby.etherscan.io/tx/0xaf0676991ff5583ac68e13197df00b7e0bfa1796f7769519721c8bff8e72ced8) |
| 8    | 0             | 30            | Pool is drained at this point                                      |


3. Once the loop breaks, I confirm that I have actually drained at least one side of the pool:

```python
# check that we have effectively drained at least one of the tokens
balance_assertion = (dex_bal1(True) == 0) or (dex_bal2(True) == 0)
print(f"Token1 balance: {dex_bal1(True)}")
print(f"Token2 balance: {dex_bal2(True)}")
print(f"at least one side is drained: {balance_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0xb05ba7ef00bcc01183a48d47c3bc8e67d81eeafcc02309676ad00ded8abfd69f
