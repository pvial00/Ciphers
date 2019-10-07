# GhostCBC - A CBC mode A-Z Block Cipher  
*** Disclaimer - This cipher is meant for entertainment and educational purposes only and should not be used to actually provide good security
The cipher operates on blocks of 16 letters.  A key and a nonce are used to create a MASHHASH equal to the block length as uses this as initialization vector for the first block.  Before this happens, a static modular arithmetic is applied to the block.  Then the block is added to the IV (or in the case of subsequent blocks, the previous block) and each value is added to an index in an internal 26 letter state indexed by K.  K is used to swap two values in the state after each block has been operated on.  Decryption is achieved by applying these steps in inverse.  

GhostCBC automatically pads data that is not equal to the block length.  

# Usage:  

from GhostCBC import GhostCBC  
GhostCBC(key).encrypt(data, nonce)  
GhostCBC(key).decrypt(data, nonce)  
