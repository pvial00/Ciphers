class Box:
    def __init__(self, width, depth, length):
        self.width = width
        self.depth = depth
        self.length = length

    def build(self):
        self.box = []
        for x in range(self.width):
            section = []
            for y in range(self.depth):
                alphabet = []
                for z in range(self.length):
                    alphabet.append((z + y + x) % self.length)
                section.append(alphabet)
            self.box.append(section)

    def load_key(self, key):
        k = []
        c = 0
        for el in key:
            k.append(ord(el) - 65)
            c = (c + (ord(el) - 65)) % 26
        return k, c

    def encrypt(self, data, key):
        ctxt = []
        k, c = self.load_key(key)
        self.build()
        klen = len(k)
        c = 0
        for byte in data:
            sub = (ord(byte) - 65)
            k.append(sub)
            sub = self.box[c][k[0]][sub]
            k.pop(0)
            ctxt.append(chr(sub + 65))
            c = (c + 1) % 26
        return "".join(ctxt)
    
    def decrypt(self, data, key):
        ctxt = []
        self.build()
        k, c = self.load_key(key)
        klen = len(k)
        c = 0
        for byte in data:
            num = (ord(byte) - 65)
            sub = self.box[c][k[0]].index(num)
            k.append(sub)
            k.pop(0)
            ctxt.append(chr(sub + 65))
            c = (c + 1) % 26
        return "".join(ctxt)
