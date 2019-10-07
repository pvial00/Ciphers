# Veruca256 Cipher v0.1.1

class Veruca:
    def __init__(self, key):
        self.mod = 256
        self.key = key
        self.keysuma = ""
        self.keysumb = 0

    def ks(self, key, nonce):
        state = range(self.mod)
        for k in key:
            kval = ord(k)
            self.keysuma += str(kval)
            self.keysumb += kval
            for x in range(kval):
                for y in range(10):
                    state.append(state.pop(kval))
                    state.append(state.pop(0))
                    state.insert(127, state.pop(2))
        for n in nonce:
            nval = ord(n)
            for x in range(nval):
                    state.append(state.pop(kval))
                    state.append(state.pop(0))
                    state.insert(127, state.pop(2))
        return state

    def encrypt(self, data, nonce=""):
        cipher_text = []
        state = self.ks(self.key, nonce)
        c = 0
        k = (int(self.keysuma) + self.keysumb) % self.mod
        for byte in data:
            sub = state[(state[state[k]]+1) % self.mod] ^ ord(byte)
            state[c], state[k] = state[k], state[c]
            k = (k + (state[state[k]] + state[c])) % self.mod
            c = (c + 1) % self.mod
            cipher_text.append(chr(sub))
        return "".join(cipher_text)

    def decrypt(self, data, nonce=""):
        return self.encrypt(data, nonce)
