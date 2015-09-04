# Wording

## How to use api
```bash
cd api
virtualenv env
. env/bin/activate
pip install flask
pip install flask-restful
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
pip install flask
pip install flask-login
pip install flask-sqlalchemy
pip install flask-mail
pip install passlib
python main.py
```
