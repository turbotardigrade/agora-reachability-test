#!/bin/sh

IP=$1

ssh ubuntu@$IP 'git clone --depth 1 https://github.com/turbotardigrade/agora nettest; cd nettest; go build; ./install_curation.sh'
