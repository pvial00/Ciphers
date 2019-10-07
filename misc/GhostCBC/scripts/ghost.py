from GhostCBC import GhostCBC
from MASHHASH import MASHMAC
from pycube import DataNormalizer, CubeKDF, CubeRandom
import sys, select, getpass, time

nonce_length = 16
mac_length = 16

try:
    mode = sys.argv[1]
except IndexError as ier:
    sys.stdout.write("Usage: python ghost.py <encrypt/decrypt> <infile> <outfile> <key>\n")
    sys.exit(1)

input_filename = sys.argv[2]
output_filename = sys.argv[3]

try:
    infile = open(input_filename, "r")
except IOError as ier:
    sys.stdout.write("Input file not found.\n")
    sys.exit(1)

try:
    outfile = open(output_filename, "w")
except IOError as ier:
    sys.stdout.write("Output file not found.\n")
    sys.exit(1)

try:
    key = sys.argv[4]
except IndexError as ier:
    key = getpass.getpass("Enter key: ")

# 256 bit key size
key = CubeKDF(keysize=64).genkey(key)

start = time.time()
buf = infile.read()
infile.close()
data = DataNormalizer().normalize(buf)

if mode == "encrypt":
    nonce = CubeRandom().random(nonce_length)
    c = GhostCBC(key).encrypt(data, nonce)
    mac = MASHMAC(length=mac_length).mac(nonce+c, key)
    outfile.write(mac+nonce+c)
elif mode == "decrypt":
    mac = data[:mac_length]
    nonce = data[mac_length:mac_length+nonce_length]
    msg = data[mac_length+nonce_length:]
    if MASHMAC(length=mac_length).verify(nonce+msg, key, mac) == True:
        plain_text = GhostCBC(key).decrypt(msg, nonce)
        outfile.write(plain_text)
    else:
        raise ValueError('MAC failed: messages has been tampered with.')
outfile.close()

end = time.time() - start
bps = len(data) / end
sys.stdout.write("Completed in "+str(end)+" seconds\n")
sys.stdout.write(str(bps)+" bytes per second.\n")
