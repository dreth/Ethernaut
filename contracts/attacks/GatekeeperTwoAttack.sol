// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract GatekeeperTwoAttack {

    constructor(address _instance) public {
        // everything runs in the constructor so that extcodesize for this contract is zero
        // when the external call to GatekeeperTwo is made

        // gatekey formed by taking first element from the bitwise XOR operation 
        // and operating it with the result of the operation in the original contract
        bytes8 gateKey = bytes8(uint64(bytes8(keccak256(abi.encodePacked(address(this))))) ^ (uint64(0) - 1));

        // run the enter function passing the gatekey
        (bool success,) = _instance.call(abi.encodeWithSignature("enter(bytes8)", gateKey));
        require(success, "external call failed");
    }
}
