class RC4A:
    def __init__(self, key):
        self.key = key

    def init(self, key):
        state = []
        for i in range(256):
            state.append(i)
        j = 0
        for i in range(256):
            j = (j + state[i] + ord(key[i % len(key)])) % 256
            state[i], state[j] = state[j], state[i]
        return state

    def crypt(self, inbuf):
        state1 = self.init(self.key)
        state2 = self.init(self.key)
        j1 = j2 = i = 0
        cipher_text = ""
        for x in range(len(inbuf)):
            i = (i + 1) % 256
            j1 = (j1 + state1[i]) % 256
            state1[i], state1[j1] = state1[j1], state1[i]
            k1 = state2[(state1[i] + state1[j1]) % 256]
            j2 = (j2 + state2[i]) % 256
            state2[i], state2[j2] = state2[j2], state2[i]
            k2 = state1[(state2[i] + state2[j2]) % 256]
            cipher_text += chr(k2 ^ (ord(inbuf[x]) ^ k1))
        return cipher_text
