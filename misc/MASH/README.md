# MASH HASH  
*** Disclaimer - This cipher is meant for entertainment and educational purposes
 only and should not be used to actually provide good security
Supports A-Z characters only  

# Usage:  

from MASHASH import MASH  
MASH(length=32).digest(data)  

# MASHBlock 
Experimental A-Z block cipher based on the MASH hash function. Operates on 16 character blocks.  Input data is automatically padded if not evenly divisible by the block length.

from MASHHASH import MASHBlock  
MASHBlock(key).encrypt(data, iv)  
MASHBlock(key).decrypt(data, iv)  

# MASHMAC
HMAC using MASH

from MASHHASH import MASHMAC  
MASHMAC().mac(data, key)  
MASHMAC().verify(data, key, mac)  
