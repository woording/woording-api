#! /bin/sh

./create-env.sh
. env/bin/activate
./reset-database.sh
python3 database_test.py
python3 database_friend_test.py
