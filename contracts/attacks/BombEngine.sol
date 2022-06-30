// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

contract BombEngine {
    function boom() public {
        selfdestruct(address(0));
    }
}
