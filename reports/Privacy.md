# Privacy

## Objectives

Unlock this contract to beat the level.

## Solution

First, the data in the `data` variable must be retrieved. This can be done by extracting the data from the contract storage as it is on the blockchain. In brownie, this can be done using `web3.eth.get_storage_at()`, with the address of the contract in the first param and the direction of the contract storage slot to look into.

Each slot has a capacity of 32 bytes (256 bits), meaning that data types which actually fill up a 32 byte slot, are going to take up a whole slot, so the following ones roll over to the next slot. If a data type is declared as `uint256` or `bytes32`, it will always occupy a full storage slot, as these types are already 32 bytes in size. 

In the case of the Privacy contract, we know that the relevant piece of data is the last element of the array `data`. Therefore, to extract this, we must determine _where_ this piece of data is, in what storage slot.

This contract's state variables are, in order:

```js
bool public locked = true;
uint256 public ID = block.timestamp;
uint8 private flattening = 10;
uint8 private denomination = 255;
uint16 private awkwardness = uint16(now);
bytes32[3] private data;
```

Therefore, the storage looks a little like this:

| slot number | object                                   | content                                                            |
|-------------|------------------------------------------|--------------------------------------------------------------------|
| 0           | locked                                   | true                                                               |
| 1           | ID                                       | block timestamp                                                    |
| 2           | flattening, denomination and awkwardness | uint16(now), 255, 100                                              |
| 3           | data[0]                                  | 0x64a6f16b073f2385269a71e47d8ae45f47d73172c5c87510274dba78b584bbaa |
| 4           | data[1]                                  | 0x9a8835c8dd1948872493737460934d6db82def5f62b1108323a69dcff6391462 |
| 5           | data[2]                                  | 0x1942e9d3378c23e90a2cc2f45bd4f1ec7f2fd8ed471d58024a3e1efe498c8ec5 |

What we're interested in is the _first 16 bytes of data[2]_, which is (in hex):

```
1942e9d3378c23e90a2cc2f45bd4f1ec
```

So then after acquiring this, all that needs to be done is simply pass it as parameter to `unlock()`, which will cause `locked` to become false.

## How I did it

Exactly as I described in [solution](#solution):

1. Get the first 16 bytes of the data in the 5th storage position of the contract instance.

```python
data_2 = web3.toBytes(hexstr=web3.eth.get_storage_at(privacy.address, '0x5').hex())[0:16].hex()
```

2. Pass it to the `unlock()` function

```python 
privacy.unlock(data_2, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x654abd57f4c71ca865d05575f9ff6356aa2940d25541cf2f53347241d6dfb0d3

3. Check that `locked` is false

```python
locked_assertion = privacy.locked() == False
print(f"The contract is unlocked: {locked_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x3e1f0abea2f84273b9a5c67b7c66562ce86601bd44ef835518ae05489d13ec96
