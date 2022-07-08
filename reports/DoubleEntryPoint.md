# DoubleEntryPoint

## Objectives

Your job is to implement a detection bot and register it in the Forta contract. The bot's implementation will need to raise correct alerts to prevent potential attacks or bug exploits.

## Solution

The vulnerability in the CryptoVault contract is present in the `sweepToken()` function. There's two ways we can sweep the DoubleEntryPoint tokens:

1. By calling `sweepToken()` and passing the DoubleEntryPoint token contract address

2. By calling `sweepToken()` and passing the LegacyToken token contract address

There's a require statement in the function which compares if this token contract address is the `underlying` token contract address defined (or modified) by the `setUnderlying()` function (which we can't call because the `underlying` token contract address is not the null address) is the DoubleEntryPoint token contract address, however, it does NOT check if it's the LegacyToken token contract address. 

When we pass the LegacyToken token contract address, the LegacyToken contract will receive the transfer call and instead delegate this transfer to the DoubleEntryPoint token contract, which will result in these tokens moving when `sweepToken()` is called.

As we can see in the DoubleEntryPoint token contract, we have the ability to use the Forta contract to create a detection bot, essentially, another contract that will trigger an alert when an otherwise unexpected event occurs. 

To protect against the CryptoVault vulnerability, we have create a detection bot contract which checks whether the CryptoVault contract is the one attempting to transfer the tokens out of the contract. If the CryptoVault address is found in the calldata of that function call, then we prevent the contract from transferring the tokens and revert the transaction by raising the alert. If the alert counter increases, then the transaction is reverted.

To do this we can either pull the data directly from the calldata by knowing where the `origSender` address (parameter of the `delegateTransfer()` function in the DoubleEntryPoint token contract) is within that calldata, so essentially what its offset is. This can be deducted by knowing how calldata is layed out. Once we know the offset, we can pull the data from that offset and compare it to the CryptoVault address. If `origSender` is the CryptoVault address, we raise the alert.

Alternatively, we can go byte by byte within that calldata until we find the offset where `origSender` is located and compare it with the CryptoVault address. Once the loop reaches this point and we successfully make the comparison, then the transaction will either continue (if `origSender` is not the CryptoVault address) or be reverted (if `origSender` is the CryptoVault address).

## How I did it

1. Get the CryptoVault contract address from the DoubleEntryPoint `cryptoVault` state variable.

```python
# get cryptovault address
cryptovault_address = dep.cryptoVault()
```

2. Instantiate the CryptoVault contract. I do this to later call `sweepToken()` in order to test my detection bot

```python
cryptovault = CryptoVault.at(cryptovault_address)
```

3. Get the Forta contract address and instantiate the Forta contract to later call `setDetectionBot()`

```python
forta = Forta.at(dep.forta())
```

4. Code and deploy (at: `0xA662bD0c21450a80c5B3fCA07709771Eb720EcB6`) DetectionBot contract that raises an alert if the CryptoVault address is found in the calldata when `sweepToken()` is called. I decided to code this using a loop which goes over every offset of the calldata (up until a max of the total size of the calldata in bytes, in this case 228 bytes). I recognize this is less efficient than simply figuring out where `origSender` is in the calldata, but I wanted to try solving the problem how I would otherwise do it in a different programming language that I'm more familiar with. This is a sort of 'bruteforce' type way to find it, but for the time being, I'm okay with that.

That said, I coded the `handleTransaction()` function as follows:

```js
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
```

The deployment is done in python as follows:

```python
bot = DetectionBot.deploy(cryptovault_address, forta.address, _from)
```

5. Set the detection bot calling `setDetectionBot()` in the forta contract with the bot contract address

```python
forta.setDetectionBot(bot.address, _from)
```

6. Get the LegacyToken token contract address to later pass it as a parameter to `sweepToken()` in CryptoVault

```python
# get the legacy token contract address
legacytoken = dep.delegatedFrom()
```

7. Try sweeping the tokens while allowing the transaction to revert 

```python
cryptovault.sweepToken(legacytoken, _from | {'allow_revert':True})
```

8. Check if the revert message is the correct one (meaning the alert was triggered)

```python
revert_msg_assertion = history[-1].revert_msg == 'Alert has been triggered, reverting'
print(f"The transaction triggered the forta alert: {revert_msg_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x3edb0cb77a9b738b830f6fe7b7b460b2a698ec70d36f66097ca71b9c7c389ce2
