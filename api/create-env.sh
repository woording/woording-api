#! /bin/bash

clear

echo "Deleting old env"
rm -rf env

echo "Creating virtualenv env"
virtualenv -p python3 env

echo "Activating env"
. env/bin/activate

echo "Installing required components using pip"
pip install flask
pip install flask-restful
pip install flask-login
pip install flask-mail
pip install flask-sqlalchemy
pip install passlib
pip install flask-httpauth
