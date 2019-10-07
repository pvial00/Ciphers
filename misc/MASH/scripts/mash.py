import sys
from MASHHASH import MASH
from pycube import DataNormalizer

infile = sys.argv[1]
try:
    in_fd = open(infile, "r")
except IOError as ier:
    print "Error: Could not open input file."
    exit(1)

try:
    key = sys.argv[2]
except IndexError as ier:
    key = ""

buf = in_fd.read()
in_fd.close()
data = DataNormalizer().normalize(buf)
h = MASH().digest(data, key)
sys.stdout.write(h+"\n")
