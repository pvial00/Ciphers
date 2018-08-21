class Rotor:
    def __init__(self, state, step,  mod=26):
        self.state = state
        self.step = step
        self.counter = 0
        self.mod = mod

    def rotate(self):
        for r in range(self.step):
            self.state.append(self.state.pop(0))
            self.counter = (self.counter + 1) % self.mod
            
    def encipher(self, num):
        return (self.state[0] + num) % self.mod

    def decipher(self, num):
        return (num - self.state[0]) % self.mod

class Wiring:
    def __init__(self, rotors):
        self.rotors = rotors

    def encipher(self, chars):
        ctxt = []
        c = 0
        for char in chars:
            sub = ord(char) - 65
            for x in range(len(self.rotors)):
                if (c % self.rotors[x].step) == 0:
                    self.rotors[x].rotate()
                    self.rotors.append(self.rotors.pop(0))
                sub = self.rotors[x].encipher(sub)
            ctxt.append(chr(sub + 65))
            c = (c + 1) % 26
        return "".join(ctxt)
    
    def decipher(self, chars):
        ctxt = []
        c = 0
        for char in chars:
            sub = ord(char) - 65
            for x in range(len(self.rotors)):
                if (c % self.rotors[x].step) == 0:
                    self.rotors[x].rotate()
                    self.rotors.append(self.rotors.pop(0))
                sub = self.rotors[x].decipher(sub)
            ctxt.append(chr(sub + 65))
            c = (c + 1) % 26
        return "".join(ctxt)

class Machine:
    
    def provision(self, key, num_rotors=26):
        keylen = len(key)
        rotors = []
        for n in range(num_rotors):
            state = range(26)
            k = ord(key[n % keylen]) - 65
            for s in range(k):
                state.append(state.pop(0))
                state[k], state[n] = state[n], state[k]
            rotor = Rotor(state, (n + 1))
            rotors.append(rotor)
        self.wiring = Wiring(rotors)

    def encipher(self, data, key):
        self.provision(key)
        return self.wiring.encipher(data)

    def decipher(self, data, key):
        self.provision(key)
        return self.wiring.decipher(data)
