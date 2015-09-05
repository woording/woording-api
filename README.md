# Wording

## Setup
Before you can run and test the code you need to have python 3 and sqlite3 installed.
You also have to execute the following lines in your terminal:
```bash
pip install flask
pip install flask-restfull
pip install flask-login
pip install flask-mail
pip install flask-sqlalchemy
pip install passlib
```

## How to use api
```bash
cd api
./reset-database.sh
virtualenv env
. env/bin/activate
sqlite3 wording.db < schema.sql
python hello.py 
```

## How to use web
```bash
cd web
python -m "SimpleHTTPServer"
open http://127.0.0.1:8000/
```

## How to use web/Leon
```bash
cd web/Leon
cd ../..

you don't use it, it's a mess
```

## How to use web/Philip
```bash
cd web/Philip
python main.py
```
