class Rotor:
    def __init__(self, state, setting, counter):
        self.state = state
        self.setting = setting
        self.counter = counter

    def step(self):
        self.counter = (self.counter + 1) % 26

    def encrypt(self, num):
        self.counter = (self.counter + 1) % 26
        return (self.state[self.counter] + num) % 26

    def decrypt(self, num):
        self.counter = (self.counter + 1) % 26
        return (num - self.state[self.counter]) % 26

class Wiring:
    def __init__(self, rotors):
        self.rotors = rotors

    def encrypt(self, chars):
        ctxt = []
        c = 0
        for char in chars:
            sub = ord(char) - 65
            for x in range(len(self.rotors)):
                self.rotors[0].step()
                if self.rotors[x].counter == 25 and x != 25:
                    self.rotors[x + 1].step()
                sub = self.rotors[x].encrypt(sub)
            ctxt.append(chr((sub + 65)))
            c = (c + 1) % 26
        return "".join(ctxt)
    
    def decrypt(self, chars):
        ctxt = []
        c = 0
        for char in chars:
            sub = ord(char) - 65
            for x in range(len(self.rotors)):
                self.rotors[0].step()
                if self.rotors[x].counter == 25 and x != 25:
                    self.rotors[x + 1].step()
                sub = self.rotors[x].decrypt(sub)
            ctxt.append(chr((sub + 65)))
            c = (c + 1) % 26
        return "".join(ctxt)

class Machine:
    def provision(self, key):
        rotors = []
        c = 1
        for k in range(len(key)):
            state = range(26)
            setting = ord(key[k]) - 65
            for s in range(setting):
                state.append(state.pop(0))
                state.insert(13, state.pop(2))
                state.insert(7, state.pop(k))
            rotors.append(Rotor(state, setting, setting))
            c += 1
        self.wiring = Wiring(rotors)

    def encrypt(self, data, key):
        self.provision(key)
        return self.wiring.encrypt(data)
    
    def decrypt(self, data, key):
        self.provision(key)
        return self.wiring.decrypt(data)
