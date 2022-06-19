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
