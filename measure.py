from subprocess import Popen, PIPE, STDOUT
from datetime import datetime

import time
import os
import sys

if len(sys.argv) != 3:
    print 'Incorrect usage. Please follow this:'
    print '\tpython measure.py [IP] [# of iterations]'
    sys.exit(1)

IP = sys.argv[1]
N = int(sys.argv[2])

ENV = os.environ.copy()
ENV["IPFS_PATH"] = "./data/MyNode"

def reset_remote_node(IP):
    p = Popen(['ssh', 'ubuntu@'+IP], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    p.stdin.write(b'cd nettest; rm -rf data; ./nettest --noPull\n')

    # return this to stop remote execution later
    def close():
        p.stdin.close()
        p.stdout.close()
        p.wait()

    for line in iter(p.stdout.readline, b''):
        if 'I am peer: ' in line:
            peer = line.split(' ')[5]

        # on receiving this we know the peer is online
        if 'Seed for' in line:
            return peer, close

def ping(peer):
    pm = Popen(['ipfs', 'ping', peer], stdout=PIPE, stderr=STDOUT, env=ENV)
    for line in iter(pm.stdout.readline, b''):
        if 'Pong received' in line:
            hasPong = True
            elapsed = time.time()-start
            pingtime = line.split(' ')[-2][5:]
            return hasPong, elapsed, pingtime
    return False, None, None

for _ in xrange(N):
    peer, close = reset_remote_node(IP)
    start, hasPong = time.time(), False
    while True:
        hasPong, elapsed, pingtime = ping(peer)
        if hasPong:
            break
    close()

    print elapsed, pingtime
    with open("times.csv", "a") as f:
        f.write("%s, %f, %s\n" % (datetime.now().time(), elapsed, pingtime))
