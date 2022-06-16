// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface IGatekeeperTwo {
    function enter(bytes8 _gateKey) external returns (bool);
}

contract GatekeeperTwoAttack {
    IGatekeeperTwo public gkt;
    uint256 contractSize;

    constructor(address _instance) public {
        gkt = IGatekeeperTwo(_instance);
    }

    function selfAwareness() public {
        uint256 sa;
        address contractAddress = address(this);
        assembly { sa := extcodesize( contractAddress ) }
        contractSize = sa;
    }

    function callEnter() public returns (bytes8){
        bytes8 gateKey = bytes8(uint64(bytes8(keccak256(abi.encodePacked(address(this))))) ^ (uint64(0) - 1));
        return gateKey;
    }
}
