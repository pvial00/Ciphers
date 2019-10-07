# GhostCBC v0.1.1
from MASHHASH import MASH

class GhostCBC:
    def __init__(self, key, mod=26, startchar=65):
        self.mod = mod
        self.startchar = startchar
        self.key = key
        self.chars = {}
        self.chars_rev = {}
        self.keysuma = 0
        self.keysumstr = ""
        self.keysumb = 0
        self.blocksize = 16
        for x in range(self.mod):
            self.chars[x] = chr(x + startchar)
            self.chars_rev[chr(x + startchar)] = x

        for k in key:
            self.keysumstr += str(self.chars_rev[k])
            self.keysumb += self.chars_rev[k]
        self.keysuma = int(self.keysumstr)

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

    def ks(self, key):
        state = range(26)
        for k in key:
            kval = self.chars_rev[k]
            for x in range(kval):
                state.append(state.pop(kval))
                state.append(state.pop(0))
                state.insert(13, state.pop(2))
        return state

    def encrypt(self, data, iv=""):
        state = self.ks(self.key)
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
                for x in range(pad):
                    block.append(pad)
            blocks.append(block)
            s += self.blocksize
            e += self.blocksize
                    
        cipher_text = []
        c = 0
        sub = 0
        bc = 0
        k = (self.keysuma + self.keysumb) % self.blocksize
        m = 0
        last = MASH(length=self.blocksize).digest(self.key+iv)
        for block in blocks:
            block[0] = (block[0] + 12) % self.mod
            block[1] = (block[1] + 4) % self.mod
            block[2] = (block[2] + 13) % self.mod
            block[3] = (block[3] + 21) % self.mod
            block[4] = (block[4] + 16) % self.mod
            block[5] = (block[5] + 2) % self.mod
            block[6] = (block[6] + 9) % self.mod
            block[7] = (block[7] + 25) % self.mod
            block[8] = (block[8] + 20) % self.mod
            block[9] = (block[9] + 5) % self.mod
            block[10] = (block[10] + 22) % self.mod
            block[11] = (block[11] + 3) % self.mod
            block[12] = (block[12] + 11) % self.mod
            block[13] = (block[13] + 1) % self.mod
            block[14] = (block[14] + 17) % self.mod
            block[15] = (block[15] + 6) % self.mod
            nextblock = ""
            for bc, b in enumerate(block):
                sub = (b + state[k]) % self.mod
                sub = (sub + self.chars_rev[last[bc % self.blocksize]]) % self.mod

                subchar = self.chars[sub]
                nextblock += self.chars[b]
                cipher_text.append(subchar)
            last = nextblock

            state[c], state[k] = state[k], state[c]
            k = (k + state[k]) % self.mod
            c = (c + 1) % self.mod
        return "".join(cipher_text)
    
    def decrypt(self, data, iv=""):
        state = self.ks(self.key)
        numblocks = len(data) / self.blocksize
        blocks = []
        s = 0
        m = 0
        e = self.blocksize
        for x in range(numblocks):
            blocks.append(self.tonumbers(data[s:e]))
            s += self.blocksize
            e += self.blocksize
        cipher_text = []
        c = 0
        sub = 0
        bc = 0
        blockc = 0
        k = (self.keysuma + self.keysumb) % self.blocksize
        j = (self.keysuma + self.keysumb) % self.mod
        last = MASH(length=self.blocksize).digest(self.key+iv)
        for block in blocks:
            nextblock = ""
            for bc, b in enumerate(block):
                sub = (b - self.chars_rev[last[bc % self.blocksize]]) % self.mod
                sub = (sub - state[k]) % self.mod
                subchar = self.chars[sub]
                nextblock += self.chars[sub]
            nb = self.tonumbers(nextblock)
            nb[0] = (nb[0] - 12) % self.mod
            nb[1] = (nb[1] - 4) % self.mod
            nb[2] = (nb[2] - 13) % self.mod
            nb[3] = (nb[3] - 21) % self.mod
            nb[4] = (nb[4] - 16) % self.mod
            nb[5] = (nb[5] - 2) % self.mod
            nb[6] = (nb[6] - 9) % self.mod
            nb[7] = (nb[7] - 25) % self.mod
            nb[8] = (nb[8] - 20) % self.mod
            nb[9] = (nb[9] - 5) % self.mod
            nb[10] = (nb[10] - 22) % self.mod
            nb[11] = (nb[11] - 3) % self.mod
            nb[12] = (nb[12] - 11) % self.mod
            nb[13] = (nb[13] - 1) % self.mod
            nb[14] = (nb[14] - 17) % self.mod
            nb[15] = (nb[15] - 6) % self.mod
            cipher_text.append("".join(self.toletters(nb)))
            last = nextblock
            if blockc == (numblocks - 1):
                padblock = nb
                padcount = padblock[len(nb) - 1]
                truecount = 0
                for x in reversed(range(len(padblock))):
                    if padblock[x] == padcount:
                        truecount += 1
                        if truecount == padcount:
                            t = cipher_text.pop()
                            trim = t[:len(t) - padcount]
                            cipher_text.append(trim)
                            break
            state[c], state[k] = state[k], state[c]
            k = (k + state[k]) % self.mod
            c = (c + 1) % self.mod
            blockc += 1
        return "".join(cipher_text)
