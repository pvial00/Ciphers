class Faster:
    def ksa(self, key, iv):
        H = []
        for char in iv:
            H.append(ord(char))
        hlen = len(H)
        keylen = len(key)
        c = 0
        for x in range(768):
            H[x % hlen] = (c + H[x % hlen] + ord(key[x % keylen])) % 256
            c = (c + H[c % hlen]) % 256
        for x in range(768):
            H[x % hlen] = (c + H[x % hlen] + ord(iv[x % keylen])) % 256
            c = (c + H[c % hlen]) % 256
        return H, c

    def hfunc(self, H, c):
        for r in range(32):
            H[r]= (H[r]+ c + 1) % 256
        return H

    def crypt(self, data, key, iv):
        H, c = self.ksa(key, iv)
        s = 0
        e = 32
        blocks = len(data) / 32
        extra = len(data) % 32
        ctxt = []
        if extra != 0:
            blocks += 1
        for n in range(blocks):
            H = self.hfunc(H, c)
            block = data[s:e]
            for b in range(len(block)):
                sub = chr(ord(block[b]) ^ H[b])
                c = c + 1
                ctxt.append(sub)
            s = s + 32
            e = e + 32
        return "".join(ctxt)
