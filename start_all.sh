#! /bin/sh

. ./stop_all.sh

pushd api 
./initialize.sh 
python3 api.py & 
popd
echo $! > api.pid


pushd web
. ../api/env/bin/activate
python3 site.py &
popd
echo $! > web.pid

