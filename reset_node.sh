#!/bin/sh

IP=$1

ssh ubuntu@$IP 'cd nettest; rm -rf data; ./nettest --noPull'
