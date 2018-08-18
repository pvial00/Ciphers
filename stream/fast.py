class Fast:
    def __init__(self, key):
        self.key = key
        self.block_size = 16
        self.rounds = 4
        self.r = 4
        seq1 = [15, 6, 5, 11, 12, 9, 10, 0, 8, 13, 2, 4, 7, 14, 1, 3]
        seq2 = [11, 10, 0, 2, 14, 1, 7, 8, 12, 6, 5, 3, 4, 15, 13, 9]
        seq3 = [5, 11, 0, 2, 1, 15, 3, 6, 12, 7, 14, 10, 9, 13, 4, 8]
        seq4 = [12, 9, 1, 4, 3, 7, 0, 5, 10, 6, 15, 14, 2, 8, 13, 11]
        self.sbox = [14,207,179, 66,123,100,103,147, 73,115,144,120,160,159,122,158,251,107,143, 79, 29,212, 51,118, 57,132,109,155,203, 48,213,254,111, 16, 87, 61,193,216,178,229, 84, 41,171, 32,151, 63,236,119,173,180,186,121, 70, 45, 98,131,219,102, 21,196, 11,163,205,228, 33,168,225,187,227,235, 69,142,133,255,185,181,175,208,191, 27,210,150, 50, 95, 42,202,244, 44,204,206,141,200,156,128, 19, 86, 83, 64, 39,137, 35,232, 65,  8,247,218,138,221,195,114,243, 78,184,  2, 28, 62,238, 55,172,189, 97,174, 75,242,165,253,222,134,113, 40,148,125,199,233,  1, 34,  0,  5,197,194, 96,176,154,101, 15,220,198,237,245, 43,167, 80, 99, 12,145, 36,214,223,153, 38, 47, 58, 37,  9, 22,252, 71,157,231, 31,152, 77, 10,161,140, 89,  6,110, 68, 18,116,169, 85,  3,234,127, 72, 88,250, 67,164, 56, 20,188,149, 92,215, 52,  4,211,217,241,112, 82, 49,166,117, 26,106,124,230,146, 59, 54, 91,226,105,240, 30, 60,108,209,162, 90,190, 93,104,246, 23,129,139, 81,239, 53,192,135, 25, 17,126, 24,249, 13, 74,183, 94,201,  7,136, 76,177,182, 46,248,170,130,224]
        self.seq = [seq1, seq2, seq3, seq4]

    def ksa(self, nonce, iv):
        #S = [0] * self.block_size
        S = []
        for i in iv:
            S.append(ord(i))
        k = 0
        n = 0
        m = 0
        self.key_length = len(self.key)
        nonce_length = len(nonce)
        l = 0
        for x in range(768):
            n = x % self.block_size
            m = x % self.key_length
            k = (k + S[k % self.block_size] + ord(self.key[m])) % self.block_size
            S[n] = (k + S[n] + ord(self.key[m])) % 256
            S[n], S[k % self.block_size] = S[k % self.block_size], S[n]
            self.sbox[x % 256], self.sbox[ord(self.key[m])] = self.sbox[ord(self.key[m])], self.sbox[x % 256]
        for x in range(768):
            n = x % self.block_size
            m = x % self.key_length
            l = x % nonce_length
            k = (k + S[k % self.block_size] + ord(nonce[l])) % self.block_size
            S[n] = (k + S[n] + ord(self.key[m])) % 256
            S[n], S[k % self.block_size] = S[k % self.block_size], S[n]
        return S, k

    def rfunc(self, S, seq):
       S[0] = (S[0] + S[seq[0]] + S[seq[14]]) % 256
       S[1] = (S[1] ^ S[seq[1]])
       S[2] = (S[2] + S[seq[2]]) % 256
       S[3] = (S[3] ^ S[seq[3]])
       S[4] = (S[4] + S[seq[4]]) % 256
       S[5] = (S[5] ^ S[seq[5]])
       S[6] = (S[6] + S[seq[6]]) % 256
       S[7] = (S[7] ^ S[seq[7]])
       S[8] = (S[8] + S[seq[8]]) % 256
       S[9] = (S[9] ^ S[seq[9]])
       S[10] = (S[10] + S[seq[10]]) % 256
       S[11] = (S[11] ^ S[seq[11]])
       S[12] = (S[12] + S[seq[12]]) % 256
       S[13] = (S[13] ^ S[seq[13]])
       S[14] = (S[14] + S[seq[14]]) % 256
       S[15] = (S[15] ^ S[seq[15]])
       return S
    
    def rfunc2(self, S, counter):
       S[0] = (S[0] + counter + 17) % 256
       S[1] = (S[1] + counter + 36) % 256
       S[2] = (S[2] + counter + 193) % 256
       S[3] = (S[3] + counter + 116) % 256
       S[4] = (S[4] + counter + 87) % 256
       S[5] = (S[5] + counter + 12) % 256
       S[6] = (S[6] + counter + 123) % 256
       S[7] = (S[7] + counter + 89) % 256
       S[8] = (S[8] + counter + 149) % 256
       S[9] = (S[9] + counter + 14) % 256
       S[10] = (S[10] + counter + 75) % 256
       S[11] = (S[11] + counter + 122) % 256
       S[12] = (S[12] + counter + 225) % 256
       S[13] = (S[13] + counter + 175) % 256
       S[14] = (S[14] + counter) % 256
       S[15] = (S[15] + counter + 201) % 256
       return S

    def combine(self, S1, S2):
       for s in range(self.block_size):
           S2[s] = (S1[s] ^ S2[s])
       return S2
           
    def crypt(self, data, nonce, iv):
       ctxt = []
       blocks = len(data) / self.block_size
       S, k = self.ksa(nonce, iv)
       start = 0
       end = self.block_size
       ctr = 0
       for x in range(blocks):
           old_S = list(S)
           block = data[start:end]
           for c, byte in enumerate(block):
              sub = ord(byte) ^ self.sbox[k]
              ctxt.append(chr((sub ^ S[c])))
              k = (k + S[c]) % 256
           S = self.rfunc2(S, ctr)
           for r in range(self.rounds):
               S = self.rfunc(S, self.seq[r % self.r])
           S = self.combine(old_S, S)
           ctr = (ctr + 1) % self.block_size
           start = (start + self.block_size)
           end = (end + self.block_size)
       return "".join(ctxt)
