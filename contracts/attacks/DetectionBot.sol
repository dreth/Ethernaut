// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "../DoubleEntryPoint.sol";

contract DetectionBot is IDetectionBot {
    address public cryptoVault;
    Forta public forta;

    constructor(address _cryptoVault, address _forta) public {
        cryptoVault = _cryptoVault;
        forta = Forta(_forta);
    }

    function handleTransaction(address user, bytes calldata) public override {
        uint dataValue;
        uint calldataloadPos = 4;
        uint _calldatasize;

        // get calldata size (in bytes) so the loop ends where the data ends
        assembly {
            _calldatasize := calldatasize()
        }

        while (calldataloadPos < _calldatasize) {
            // obtain the next 32-byte item from the calldata
            assembly {
                dataValue := calldataload(calldataloadPos)
            }

            // check if the address is present in the next 32 byte slot
            if (dataValue == uint256(uint160(cryptoVault))) {
                // raise alert if address is present in calldata
                forta.raiseAlert(user);
                break;

            } else {
                // add one to calldataloadpos
                assembly {
                    calldataloadPos := add(calldataloadPos, 0x1)
                }
            }
        }
    }
}
