from pycube import CubeKDF

class MASH:
    def __init__(self, length=32):
        self.chars = {}
        self.chars_rev = {}
        for x in range(26):
            self.chars[x] = chr(x + 65)
            self.chars_rev[chr(x + 65)] = x
        self.iv = []
        self.length = length
        self.ivchar = 0
        for i in range(self.length):
            self.iv.append(self.ivchar)

    def tonumbers(self, letters):
        n = []
        for l in letters:
            n.append(self.chars_rev[l])
        return n

    def digest(self, data, key=""):
        state = range(26)
        buf = self.tonumbers(data)
        buf.extend(self.iv)
        keysum = 0
        h = []
        for i in range(self.length):
            h.append(self.ivchar)
        if key != "":
            for c, char in enumerate(key):
                cval = self.chars_rev[char]
                keysum += cval
                for r in range(cval):
                    state.append(state.pop(0))
                    state.append(state.pop(cval))
                    state.insert(13, state.pop(2))
        last = keysum
        for b in buf:
            last += b ^ (b + 65)

        for c, b in enumerate(buf):
            j = (b + last) % 26
            z = ((b ^ last) + state[(state[last % 26] + state[b]) % 26]) % 26
            last = z
            x = b % self.length
            h[c % self.length] = z
            h[x] = (b + h[x]) % 26
            state[c % 26], state[j] = state[j], state[c % 26]
        return "".join((self.chars[a]) for a in h)

class MASHMAC:
    def __init__(self, length=16):
        self.length = length

    def mac(self, data, key):
        k1 = CubeKDF().genkey(key)
        k2 = CubeKDF().genkey(k1)
        h1 = MASH(self.length).digest(data, k2)
        h2 = MASH(self.length).digest(h1, k1)
        return h2

    def verify(self, data, key, mac):
        m = self.mac(data, key)
        if m == mac:
            return True
        else:
            return False

class MASHBlock:
    def __init__(self, key, blocksize=16, mod=26, startchar=65):
        self.mod = mod
        self.key = key
        self.chars = {}
        self.chars_rev = {}
        self.blocksize = blocksize
        for x in range(self.mod):
            self.chars[x] = chr(x + startchar)
            self.chars_rev[chr(x + startchar)] = x

    def tonumbers(self, letters):
        n = []
        for l in letters:
            n.append(self.chars_rev[l])
        return n

    def toletters(self, numbers):
        l = []
        for n in numbers:
            l.append(self.chars[n])
        return l

    def encrypt(self, data, iv=""):
        numblocks = len(data) / self.blocksize
        if len(data) < self.blocksize:
            extrablock = self.blocksize - len(data)
        else:
            extrablock = len(data) % self.blocksize
        if extrablock != 0:
            extra = 1
        else:
            extra = 0
        blocks = []
        s = 0
        e = self.blocksize
        for x in range(numblocks+extra):
            block = self.tonumbers(data[s:e])
            if len(block) < self.blocksize:
                pad = self.blocksize - len(block)
                for y in range(pad):
                        block.append(pad)
            blocks.append(block)
            s += self.blocksize
            e += self.blocksize
                    
        cipher_text = []
        blockc = 0
        c = 0
        sub = 0
        bc = 0
        hasher = MASH(length=self.blocksize)
        h = hasher.digest(self.key+iv)
        for block in blocks:
            for b in block:
                sub = (b + self.chars_rev[h[bc % self.blocksize]]) % 26
                bc = (bc + 1) % self.mod
                cipher_text.append(self.chars[sub])
            h = hasher.digest(h+self.chars[c])
            c = (c + 1) % self.mod
            blockc += 1
        return "".join(cipher_text)
    
    def decrypt(self, data, iv=""):
        numblocks = len(data) / self.blocksize
        blocks = []
        s = 0
        e = self.blocksize
        for x in range(numblocks):
            blocks.append(self.tonumbers(data[s:e]))
            s += self.blocksize
            e += self.blocksize
        cipher_text = []
        blockc = 0
        c = 0
        sub = 0
        bc = 0
        hasher = MASH(length=self.blocksize)
        h = hasher.digest(self.key+iv)
        for block in blocks:
            for b in block:
                sub = (b - self.chars_rev[h[bc % self.blocksize]]) % 26
                bc = (bc + 1) % self.mod
                cipher_text.append(self.chars[sub])
            if blockc == (numblocks - 1):
                padblock = cipher_text[len(cipher_text) - (self.blocksize):]
                padcount = self.chars_rev[padblock[len(block) - 1]]
                truecount = 0
                for x in reversed(range(len(padblock))):
                    if self.chars_rev[padblock[x]] == padcount:
                        truecount += 1
                        if truecount == padcount:
                            break
                if padcount == truecount:
                    for x in range(truecount):
                        t = cipher_text.pop()
            h = hasher.digest(h+self.chars[c])
            c = (c + 1) % self.mod
            blockc += 1
        return "".join(cipher_text)
