# Fold
Custom binary encoding using up to 67 bytes in a character set  
Padding is enabled by default and decode is not supported without it just yet.  

The encoding can be keyed so that only the holder of the key can unlock the encoding.  Binary keys are supported.  

# Usage:  
from Fold import Fold  
Fold().encode(data)  
Fold().decode(data)  

With keys:  

Fold(key).encode(data)  
Fold(key).decode(data)  

Using PRG:  

Fold(key, prg=True).encode(data)  
Fold(key, prg=True).decode(data)  

# Example encoding  
We hold these truths to be self-evident, that all men are created equal  
VYZaI=a=beb=Z=I=d=a=ZacfZaI=d=ceded=a=cfI=d=beI=YaZaI=cfZab=ZbLMZadfabZ=Zabdd=L=I=d=a=YZd=I=YZb=b=I=bcZabdI=YZceZaI=YbceZaYZd=ZaZ=I=ZacddeYZb=  
