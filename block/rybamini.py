import os

def getAZrandom(length):
    l = 0
    c = []
    while True:
        if l == length:
            break
        sample = ord(os.urandom(1))
        if sample >= 0 and sample <= 25:
            unit = chr(sample + 65)
            l = l + 1
            c.append(unit)
        else:
            pass
    return "".join(c)

class RybaMini:
    blocksize = 12
    rounds = 32
    ivlen = 24
    def keytok(self, key):
        k = []
        j = 0
        for char in key:
            p = ord(char) - 65
            k.append(p)
            j = (j + p) % 26
        return k, j

    def tonums(self, chars):
        n = []
        for char in chars:
            p = ord(char) - 65
            n.append(p)
        return n

    def tochars(self, num):
        c = []
        for n in num:
            p = chr(n + 65)
            c.append(p)
        return "".join(c)
    
    def add(self, a, b):
        for x in range(len(a)):
            a[x] = (a[x] + b[x]) % 26
        return self.tochars(a)
    
    def sub(self, a, b):
        for x in range(len(a)):
            a[x] = (a[x] - b[x]) % 26
        return self.tochars(a)

    def rotate(self, block, r):
        for x in xrange(r):
            block.append(block.pop(0))
        return block
            
    def gen_sbox(self, key):
        k = range(26)
        kp, j = self.keytok(key)
        klen = len(kp)
        i = 0
        c = 0
        S = []
        for x in range(338):
            k[x % 26] = (k[x % 26] + kp[i]) % 26
            i = (i + 1) % klen
        for x in range(self.blocksize):
            box = range(26)
            for y in range(338):
                j = k[j]
                k[j] = (k[j] + k[c]) % 26
                o = (k[j] + k[k[j]]) % 26
                box[c], box[o] = box[o], box[c]
                c = (c + 1) % 26
            S.append(box)
        return S, k, j
    
    def gen_keys(self, k, j):
        K = []
        c = 0
        for x in range(self.rounds):
            key = []
            for y in range(self.blocksize):
                j = k[j]
                k[j] = (k[j] + k[c]) % 26
                o = (k[j] + k[k[j]]) % 26
                c = (c + 1) % 26
                key.append(o)
            K.append(key)
        return K

    def block_encrypt_ofb(self, block, S, K):
        left = block[:self.blocksize]
        right = block[self.blocksize:]
        for r in range(self.rounds):
            for b in range(self.blocksize):
                left[b] = S[b][left[b]]
                right[b] = (right[b] + K[r][b]) % 26
                left[b] = (left[b] + right[b]) % 26
                right[b] = (right[b] + left[b]) % 26
            left = self.rotate(left, 3)
            tmp = left
            left = right
            right = tmp
        return left+right
    
    def encrypt(self, chars, key):
        S, k, j = self.gen_sbox(key)
        K = self.gen_keys(k, j)
        blocks = len(chars) / (self.blocksize * 2)
        extrablocks = len(chars) % (self.blocksize * 2)
        s = 0
        e = self.blocksize * 2
        ivtmp = getAZrandom(self.ivlen)
        iv = self.tonums(ivtmp)
        ctxt = []
        for x in range(blocks):
            block = chars[s:e]
            s += self.blocksize * 2
            e += self.blocksize * 2
            iv = self.block_encrypt_ofb(iv, S, K)
            block = self.add(self.tonums(block), iv)
            ctxt.append(block)
        return "".join(ctxt)
    
    def decrypt(self, chars, key, iv):
        S, k, j = self.gen_sbox(key)
        K = self.gen_keys(k, j)
        blocks = len(chars) / (self.blocksize * 2)
        extrablocks = len(chars) % (self.blocksize * 2)
        s = 0
        e = self.blocksize * 2
        ivtmp = self.tonums(iv)
        ctxt = []
        for x in range(blocks):
            block = chars[s:e]
            s += self.blocksize * 2
            e += self.blocksize * 2
            ivtmp = self.block_encrypt_ofb(ivtmp, S, K)
            block = self.sub(self.tonums(block), ivtmp)
            
            ctxt.append(block)
        return "".join(ctxt)
