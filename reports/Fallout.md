# Fallout

The fallout challenge has the following sole objective:

1. you claim ownership of the contract

## Solution

The constructor method for this contract is not really a constructor, as it is neither using the `constructor()` function, nor labeling what is supposed to be the constructor function `Fal1out()` with the right name (`Fallout()`).

To solve this, all we have to do is call the `Fal1out()` function.

## How I did it

1. Call the `Fal1out()` function with a value of 0.

```python
fallout.Fal1out(_from | {'value':0})
```

Tx hash: https://rinkeby.etherscan.io/tx/0xbfc58f91420dd07d7fd61238a5bf240a8cda8660462cf4c7527781a64eba7818


### Submission transaction

Tx hash: https://rinkeby.etherscan.io/tx/0x1e38a8643d2daf32da8841c457d09e68ce397929dc5456cbf8277606e33d8fa5
