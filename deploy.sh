#! /bin/bash

ssh cor@woording.com -t 'cd /home/cor/server/woording/woording-api;
screen -X -S api kill;
git pull;
screen -S api -m "/home/cor/server/woording/woording-api/start-server.sh";'

echo 'Finished'
