#!/usr/bin/env python
import atexit
import os
import random
import time
from struct import pack

def write_channel(f, gamma, gmin, gmax):
    f.write(pack('!I', int(gamma * 65536)))
    f.write(pack('!I', int(gmin * 65536)))
    f.write(pack('!I', int(gmax * 65536)))

def write_vcgt(filename, red, green, blue):
    f = file(filename, 'w')
    tagOffset = 144 # start right after header
    tagSize = 0
    f.write('.' * 128)
    f.write(pack('!I', 1)) # num tags as int
    f.write("vcgt") # tag name
    f.write(pack('!I', tagOffset)) # offset as int
    f.write(pack('!I', tagSize)) # size as int

    f.write("vcgt") # tag name again
    f.write(pack('!I', 0)) # ignored by xcalib
    f.write(pack('!I', 1)) # gamma type: VideoCardGammaFormula
    write_channel(f, *red)
    write_channel(f, *green)
    write_channel(f, *blue)
    f.close()

def gradient(start, end, step, total):
    result = []
    for i in range(len(start)):
        current = []
        for j in range(len(start[i])):
            current.append(start[i][j] + step * (end[i][j] - start[i][j]) / total)
        result.append(current)

    return result

def xcalib(data):
    icc_filename = "/tmp/psychreen.icc"
    write_vcgt(icc_filename, *data)
    os.system("xcalib %s" % icc_filename)

def get_next():
    result = []
    for i in range(3):
        #result.append((random.random() * 5.0, random.random(), random.random()))
        result.append((random.random() * 5.0, 0.0, 1.0))
    return result

def main():
    current = [(1.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, 1.0)]
    next = get_next()
    total = 50
    while True:
        for i in range(total):
            xcalib(gradient(current, next, i, total))
            time.sleep(0.05)

        current, next = next, get_next()

def cleanup():
    os.system("xcalib -c")
    pass

if __name__ == "__main__":
    atexit.register(cleanup)
    main()
