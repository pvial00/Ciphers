# Machine2620

Machine2620 is a rotor based cipher machine cipher that operates on characters A-Z like classic rotor machines of the past.

The machine is composed of 26 rotors, 26 multiplexers, a substitution board and grid lock.

Each rotor indivdiually encrypts a plain text character and permutes itself upon encryption or decryption of a character.

Each multiplexer decides the signal path to the next rotor based on a keyed pattern based on the machine settings.

The substitution board serves as a static A-Z substitution table that is used at the very end of the encryption and decryption process.

The GridLock is a transposition procedure that is independently keyed.  It operates on blocks of 26 characters, rearranges the characters, substitutes them and then rearranges the blocks of 26 characters in a specific keyed order.

*** This machine is intentionally designed to operate slowly

# Example use

key = "HELLOWORLD"

grid_key = "MACHINE"

settings = [[1, 12, 6], [8, 15, 1], [25, 8, 2], [9, 0, 3], [3, 7, 0], [4, 1, 6], [8, 4, 5], [6, 6, 3], [2, 9, 4], [22, 11, 14], [15, 4, 17], [9, 16, 7], [24, 8, 0], [1, 12, 6], [8, 15, 1], [25, 8, 2], [9, 0, 3], [3, 7, 0], [4, 1, 6], [11, 24, 7], [19, 18, 4], [13, 7, 9], [20, 19, 20], [1, 13, 14], [10, 2, 18], [21, 16, 5]]

m = Machine2620(settings, key, grid_key)

ctxt = m.encrypt(msg)

m2 = Machine2620(settings, key, grid_key)
ptxt = m2.decrypt(ctxt)

