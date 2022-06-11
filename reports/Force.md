# Force

## Objectives

The goal of this level is to make the balance of the contract greater than zero.

## Solution

From my research, there's several ways of sending funds to a contract that has no `payable` methods:

1. Send funds to the address the contract will be deployed in, because contract addresses are deterministic.

2. Send funds to the contract by destroying of another contract, which sends all of its balance through `selfdestruct(<destination>)`.

3. By making it the recipient of a block reward, which can't be rejected.

Because the instance of the Force contract is already deployed, the easiest way we can complete the objective is through number 2.

## How I did it

1. Deploy an attacking contract called ForceAttack (at: `0xba2C7CAE436F3710500507d1f5cf07229C3d0C66`)

```python
forceattack = ForceAttack.deploy(_from)
```

And make sure the contract can receive funds and also has a function that calls `selfdestruct()` to the contract address of our instance:

```cs
function reload() external payable {}

function forceEtherIntoAddress(address payable _to) external onlyOwner {
    selfdestruct(_to);
}
```

I also optionally added a fallback `receive()` function and made the contract `Ownable` so that only I could call the `selfdestruct()` function (not that anyone would've done it anyway...)

2. Send some funds into the contract.

```python
forceattack.reload({'value': 1000} | _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xcd6a2d6d2e618742a61f919924ac1093fc92b942ee6b22ce95f5961505b9df49

3. Call the function that calls `selfdestruct()` designating my instance address as the recipient of the funds.

```python
forceattack.forceEtherIntoAddress(force.address)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x936c5b1b5131c445f80eb7e38c1d1c766e8134a06c07613b07a7524f33da0faa

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x1e38a8643d2daf32da8841c457d09e68ce397929dc5456cbf8277606e33d8fa5
