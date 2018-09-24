class H2:
    def keysetup(self, key):
        k = []
        j = 0
        for c in key:
            k.append(ord(c) - 65)
            j = (j + (ord(c) - 65)) % 26
        return k, j

    def encrypt(self, chars, key):
        ctxt = []
        k, j = self.keysetup(key)
        klen = len(k)
        c = 0
        i = 0
        last = j
        for x, char in enumerate(chars):
            j = (j + last + c) % 26
            k.append(j)
            num = ord(char) - 65
            sub = (num + k.pop(0)) % 26
            last = sub
            ctxt.append(chr(sub + 65))
            c = (c + 1) % 26
        return "".join(ctxt)
    
    def decrypt(self, chars, key):
        ctxt = []
        k, j = self.keysetup(key)
        klen = len(k)
        last = j
        c = 0
        for x, char in enumerate(chars):
            num = ord(char) - 65
            j = (j + last + c) % 26
            k.append(j)
            sub = (num - k.pop(0)) % 26
            last = num
            ctxt.append(chr(sub + 65))
            c = (c + 1) % 26
        return "".join(ctxt)
