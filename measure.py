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
        if 'peer identity: ' in line:
            peer = line[15:-1]

        # on receiving this we know the peer is online
        if 'Seed for' in line:
            return peer, close

for _ in xrange(N):
    peer, close = reset_remote_node(IP)
    start, hasPong = time.time(), False
    while not hasPong:
        pm = Popen(['ipfs', 'ping', peer], stdout=PIPE, stderr=STDOUT, env=ENV)
        for line in iter(pm.stdout.readline, b''):
            if 'Pong received' in line:
                hasPong = True
                elapsed = time.time()-start
                ping = line.split(' ')[-2][5:]
                break
            pm.wait()

        # print 'No Pong. Restart...'
    close()

    print elapsed, ping
    with open("times.csv", "a") as f:
        f.write("%s, %f, %s\n" % (datetime.now().time(), elapsed, ping))
