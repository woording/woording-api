#! /bin/bash

clear
echo "Reset database"

echo "Deleting old database"
rm -rf wording.db

echo "Creating new database"
touch wording.db

echo "Inserting schema.sql into new database"
sqlite3 wording.db < schema.sql


