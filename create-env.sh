#! /bin/bash

clear

echo "Deleting old env"
rm -rf env

echo "Creating virtualenv env"
virtualenv -p python3 env

echo "Activating env"
. env/bin/activate

echo "Installing required components using pip"
pip3 install flask
pip3 install flask-restful
pip3 install flask-login
pip3 install flask-mail
pip3 install flask-cors
pip3 install flask-sqlalchemy
pip3 install passlib
pip3 install validate_email
pip3 install flask-httpauth
