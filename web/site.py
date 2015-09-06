# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def render():
    return render_template("index.html")

@app.route('/<username>')
def reroute(username):
    return render_template("index.html", username=username)

if __name__ == '__main__':
    app.run(port=5001)
