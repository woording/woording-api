#! /bin/sh

./reset-database.sh
./create-env.sh
python3 database_test.py

clear
