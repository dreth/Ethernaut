# MagicNumber

## Objectives

To solve this level, you only need to provide the Ethernaut with a Solver, a contract that responds to whatIsTheMeaningOfLife() with the right number.

## Solution

There's several ways to approach this problem, but in a nutshell, all that's needed is a contract that can return the number 42 by using _at most_ 10 opcodes in its _runtime_ code.

I find that [this article](https://medium.com/coinmonks/ethernaut-lvl-19-magicnumber-walkthrough-how-to-deploy-contracts-using-raw-assembly-opcodes-c50edb0f71a2) details the solution much better than I could. But as a way to document my understanding of this problem and its solution, I'll try to write in a few steps what has to be done to successfully solve it:

1. We must code a contract using either raw bytecode or Yul (as I did in [my solution](#how-i-did-it)):

```
33600055600a6011600039600a6000f3fe602a60005260206000f3
```

Which is the raw bytecode representing the following opcodes:

```
CALLER PUSH1 0x0 SSTORE PUSH1 0xA PUSH1 0x11 PUSH1 0x0 CODECOPY PUSH1 0xA PUSH1 0x0 RETURN INVALID PUSH1 0x2A PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 RETURN 
```

These raw assembly opcodes can be divided into two parts:

* Initialization code (can be of any length)

```assembly
CALLER PUSH1 0x0 SSTORE PUSH1 0xA PUSH1 0x11 PUSH1 0x0 CODECOPY PUSH1 0xA PUSH1 0x0 RETURN INVALID
```

* Runtime code (has to have a length of _at most_ 10 opcodes)

```assembly
PUSH1 0x2A PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 RETURN 
```

Here's the bytecode as returned by the Remix IDE after compiling the Yul contract I coded to solve this:

```json
{
	"functionDebugData": {},
	"generatedSources": [],
	"linkReferences": {},
	"object": "33600055600a6011600039600a6000f3fe602a60005260206000f3",
	"opcodes": "CALLER PUSH1 0x0 SSTORE PUSH1 0xA PUSH1 0x11 PUSH1 0x0 CODECOPY PUSH1 0xA PUSH1 0x0 RETURN INVALID PUSH1 0x2A PUSH1 0x0 MSTORE PUSH1 0x20 PUSH1 0x0 RETURN ",
	"sourceMap": "90:8:0:-:0;87:1;80:19;143;120:21;117:1;108:55;182:19;179:1;172:30"
}
```

2. Deploy the contract to the blockchain, which we can do in several different possible ways:

* Writing the contract in Yul and using the Yul compiler on the Remix IDE and then deploying the blockchain using injected Web3 or any other method.

* Creating a contract that itself deploys a contract on the blockchain using raw bytecode and calling either `create()` or `create2()` in an `assembly{}` block on the contract.

* Sending a raw transaction with the bytecode as data, which the EVM will interpret as a contract creation from the set of initialization opcodes.

There are probably more ways, but I'm not familiar with them.

1. Set the solver calling `setSolver()` in the MagicNum contract.

## How I did it

1. I first needed to look for help as I had absolutely no idea how to approach this problem, but after extensive reading of how this whole thing works and some basics of opcodes and EVM assembly, I then decided to code a contract using Yul (deployed at: `0x678a4e09ec08d8fd32abc0f4e3e28469fe8b6e80`), which IMO is a very readable way of attempting to do this.

The contract looks like this (It's under `/contracts/attacks/MagicNumberSolver.Yul` in the repo):

```Yul
// SPDX-License-Identifier: MIT
object "MagicNumberSolver" {
    code {
        sstore(0, caller())
        datacopy(0, dataoffset("Runtime"), datasize("Runtime"))
        return(0, datasize("Runtime"))
    }
    object "Runtime" {
        code {
            mstore(0x0, 0x2a)
            return(0x0, 0x20)    
        }
    }
}
```

This is a _million times_ more readable than raw bytecode or even raw opcodes, though now raw opcodes no longer look like robot instructions to me (even though they technically are). 

This is the constructor of the contract (initialization opcodes), usually declared with `constructor()` in Solidity:

```Yul
code {
    sstore(0, caller())
    datacopy(0, dataoffset("Runtime"), datasize("Runtime"))
    return(0, datasize("Runtime"))
}
```

This code basically stores the `caller()` in slot 0 and copies the contract code ("Runtime") to it (`datacopy()`) and specifying the size of the contract code (`datasize()`) and the offset (`dataoffset()`). The name of the object containing the code (in my case "Runtime") can be anything, it simply serves as a way to refer to it through functions like `datasize()`, which take a string of the name of a Yul object. The return opcode concludes the runtime of the constructor.

And this is the code of the contract itself after deployment (runtime opcodes), what is stored on the blockchain:

```
object "Runtime" {
    code {
        mstore(0x0, 0x2a)
        return(0x0, 0x20)    
    }
}
```

This object also has code, and this code is also extremely short, but does what we are asked for in the exercise as requested, which is first allocate memory (`mstore`) on slot `0x0` with the value `0x2a` which is the number 42 in hexadecimal. Then it takes that value in slot `0x0` and `return`s it as `0x20` which is 32 bytes.

Subsequently, I compiled and deployed the contract using the Remix IDE, which has a Yul compiler marked as experimental at the time of solving this challenge.

2. Call the `setSolver()` function to set the solver to the address of the deployed contract

```python 
magicnumber.setSolver('0x678a4e09ec08d8fd32abc0f4e3e28469fe8b6e80', _from)
```

Block explorer: https://rinkeby.etherscan.io/tx/0x39dd993c53234338ad6928550cfc73040081da7007c11ae15c5a05fbbd3e116f

3. The only way to confirm this works is to either make a set up of the Ethernaut challenges locally, or just attempt to submit on the Ethernaut site, and I decided to just submit, since it can be attempted again anyway even if it's wrong. In my case, I made a few attempts tweaking different values until I got it right, my biggest error was that in the "Runtime" object I was writing numbers in decimal instead of hexadecimal.

### Submission transaction

Block explorer: https://rinkeby.etherscan.io/tx/0xc46148d557083fb12b8768884f70091d3099f535ae20281edc8a6f8018a7c5f5
