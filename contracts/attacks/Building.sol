// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

interface IElevator {
    function goTo(uint256 _floor) external;
    function floor() external returns (uint256);
}

contract Building {
    IElevator public elevatorContract;
    uint8 public topFloor = 1;
    bool public lastFloorBool;

    constructor(address _instance) {
        elevatorContract = IElevator(_instance);
    }


    function isLastFloor(uint256) external returns (bool) {
        lastFloorBool = elevatorContract.floor() == topFloor;
        return lastFloorBool;
    }

    function goToTopFloor() external {
        elevatorContract.goTo(topFloor);
    }
}
