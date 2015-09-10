#! /bin/sh

./create-env.sh
. env/bin/activate
./reset-database.sh
python3 database_test.py
