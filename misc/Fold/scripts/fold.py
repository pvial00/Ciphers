import sys, select, getpass, os, time, getopt, hashlib
from Fold import Fold

def usage():
    msg = "Usage: python fold.py (encode/decode) <infile> <outfile> <optional key>"
    sys.stdout.write(msg+"\n")

try:
    mode = sys.argv[1]
except IndexError as ier:
    usage()
    sys.exit(1)

input_filename = sys.argv[2]
output_filename = sys.argv[3]

try:
    infile = open(input_filename, "r")
except IOError as ier:
    usage()
    sys.exit(1)

try:
    outfile = open(output_filename, "w")
except IOError as ier:
    usage()
    sys.exit(1)

try:
    key = sys.argv[4]
except IndexError as ier:
    key = ""
    prgmode = False
else:
    salt = hashlib.sha256(key).digest()
    key = hashlib.pbkdf2_hmac('md5', key, salt, 100000)
    prgmode = True

start = time.time()
data = infile.read()
infile.close()

if mode == "encode":
    outfile.write(Fold(key, prg=prgmode).encode(data))
elif mode == "decode":
    decoded = Fold(key, prg=prgmode).decode(data)
    outfile.write(decoded)
outfile.close()

end = time.time() - start
bps = len(data) / end
sys.stdout.write("Completed in "+str(end)+" seconds\n")
sys.stdout.write(str(bps)+" bytes per second.\n")
