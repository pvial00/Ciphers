class Rotor(object):
    def __init__(self, key, rid):
        self.rid = rid
        self.state = list(range(26))
        self.i = rid
        self.j = 0
        self.k = [0] * 26
        for i, char in enumerate(key):
            self.k[i] = ((ord(char) - 65) + self.k[i]) % 26
        self.ks(self.k)
        
    def ks(self, key):
       i = self.i
       j = 0
       for x in range(26):
           self.state[i], self.state[j] = self.state[j], self.state[i]
           j = (self.state[self.k[self.state[self.k[i]]]] + self.k[i] + self.state[j] + self.rid) % 26
           i = (i + self.state[self.state[i]]) % 26
       self.i = i
       self.j = j

    def enc(self, char, i):
        self.step()
        return (self.state[i] + char) % 26

    def dec(self, char, i):
        self.step()
        return (char - self.state[i]) % 26

    def step(self):
        self.state[self.i], self.state[self.j] = self.state[self.j], self.state[self.i]
        self.i = (self.i + self.state[self.i]) % 26
        self.j = (self.state[self.k[self.state[self.k[self.i]]]] + self.k[self.i] + self.state[self.j]) % 26
        self.k[self.j] = (self.k[self.j] + self.j) % 26

class Multiplexer(object):
    def __init__(self, settings, key, mid):
        self.s0 = settings[0]
        self.s1 = settings[1]
        self.s2 = settings[2]
        self.i = self.s0
        self.l = self.s1
        self.pathway = list(range(26))
        for x in range(26 * self.s2):
            self.reroute()

    def reroute(self):
        self.i = (self.i + self.pathway[self.i]) % 26
        self.pathway[self.l], self.pathway[self.pathway[self.i]] = self.pathway[self.pathway[self.i]], self.pathway[self.l]

    def route(self, i):
        self.l = (self.l + i) % 26
        return self.pathway[i]

class SubBoard(object):
    def __init__(self, key):
       self.state = list(range(26))
       self.k = [0] * 26
       self.j = 0
       self.i = 0
       for i, char in enumerate(key):
           self.k[i] = ((ord(char) - 65) + self.k[i]) % 26
           self.j = (self.j + self.k[i]) % 26
       self.ks(self.k)

    def ks(self, key):
       i = self.i
       j = self.j
       for x in range(54):
           self.state[i], self.state[j] = self.state[j], self.state[i]
           j = (self.state[self.k[self.state[self.k[i]]]] + self.k[i] + self.state[j]) % 26
           i = (i + self.state[self.state[i]]) % 26
       self.i = i
       self.j = j

    def enc(self, char):
        return self.state[char]

    def dec(self, char):
        return self.state.index(char)

class GridLock(object):
    def __init__(self, key, textlen, mode):
        self.g = []
        self.bs = 26
        self.gridsize = int(textlen / self.bs)
        self.gridextra = (self.bs) - int(textlen % self.bs)
        self.gridextrachars = int(textlen % self.bs)
        self.textlen = textlen
        self.textlen += self.gridextra
        if self.gridextrachars != 0 and mode == 0:
            self.gridsize += 1
        if textlen < self.bs:
            self.gridsize = 1
        self.iterations = 26 * self.bs
        for x in range(self.gridsize):
            grid = []
            for y in range(self.bs):
                grid.append(0)
            self.g.append(grid)
        self.ks(key)

    def ks(self, key):
        self.k = 0
        self.s = list(range(26))
        j = 0
        c = 0
        for x in range(len(key)):
            j = (j + ord(key[x])) % 26
        for x in range(self.iterations):
            self.s[j], self.s[c] = self.s[c], self.s[j]
            j = (j + self.s[self.s[j]]) % 26
            self.k = (self.k + j) % self.gridsize
            c = (c + 1) % 26
        self.j = j

    def order_gen(self):
        self.o = list(range(self.gridsize))
        c = 0
        for x in range(26 * self.gridsize):
            self.o[self.k], self.o[c] = self.o[c], self.o[self.k]
            self.k = (self.k + self.o[self.k] + 1) % self.gridsize
            c = (c + 1) % self.gridsize

    def pad(self, text):
        t = list(text)
        if self.gridextrachars != 0:
            for x in range(self.gridextra):
                t.append(chr(self.gridextra + 65))
        return "".join(t)

    def unpad(self, text):
        t = list(text)
        last = ord(t[len(t) - 1]) - 65
        pos = len(t) - 1
        c = 0
        for x in range(last):
            sample = ord(t[pos]) - 65
            pos -= 1
            if sample == last:
                c += 1
        if c == last:
            t = t[:len(text) - last]
        return "".join(t)
 
    def lock(self, text):
        text = self.pad(text)
        self.order_gen()
        c = 0
        gridtext = []
        for x in range(self.gridsize):
            Gpos = self.o[x]
            for y in range(self.bs):
                sub = self.s[ord(text[c]) - 65]
                Spos = self.s[y]
                self.g[Gpos][Spos] = chr(sub + 65)
                c += 1
        for x in range(self.gridsize):
            for y in range(self.bs):
                gridtext.append(self.g[x][y])
        return "".join(gridtext)

    def unlock(self, text):
        self.order_gen()
        c = 0
        gridtext = []
        for x in range(self.gridsize):
            Gpos = self.o.index(x)
            for y in range(self.bs):
                sub = self.s.index(ord(text[c]) - 65)
                Spos = self.s.index(y)
                self.g[Gpos][Spos] = chr(sub + 65)
                c += 1
        for x in range(self.gridsize):
            for y in range(self.bs):
                gridtext.append(self.g[x][y])
        return self.unpad("".join(gridtext))

class Wiring(object):
    def __init__(self, settings, key):
        self.r = []
        self.m = []
        for x in range(26):
            self.r.append(Rotor(key, x))
            self.m.append(Multiplexer(settings[x], key, x))
        self.s = SubBoard(key)
        
    def enc(self, char):
        num = ord(char) - 65
        i = 0
        c = 0
        for x in range(26):
            num = self.r[i].enc(num, i)
            self.m[c].reroute()
            i = self.m[c].route(c)
            c = (c + 1) % 26
        self.shift(i)
        self.s.enc(num)
        return chr(num + 65)

    def dec(self, char):
        num = ord(char) - 65
        i = 0
        c = 0
        for x in range(26):
            num = self.r[i].dec(num, i)
            self.m[c].reroute()
            i = self.m[c].route(c)
            c = (c + 1) % 26
        self.shift(i)
        self.s.dec(num)
        return chr(num + 65)

    def shift(self, iterations):
        i = 0
        for x in range(iterations):
            i = (i + self.r[x].i) % 26
            self.r.append(self.r.pop(i))

class Machine2620(object):
    def __init__(self, settings, key, grid_key):
        self.wiring = Wiring(settings, key)
        self.grid_key = grid_key

    def encrypt(self, chars):
        grid = GridLock(self.grid_key, len(chars), 0)
        chars = grid.lock(chars)
        ctxt = []
        for char in chars:
            ctxt.append(self.wiring.enc(char))
        return "".join(ctxt)

    def decrypt(self, chars):
        grid = GridLock(self.grid_key, len(chars), 1)
        ptxt = []
        for char in chars:
            ptxt.append(self.wiring.dec(char))
        chars = grid.unlock("".join(ptxt))
        return chars
