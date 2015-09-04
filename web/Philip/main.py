from flask import Flask, request, session, render_template, abort, redirect, url_for, flash
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
import os
 
SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
 
db = SQLAlchemy(app)

# Database class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

# Initialize database
@app.before_first_request
def init_request():
    db.create_all()

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None

# Main page
@app.route('/')
def index():
    return render_template('index.html')

# User login handler
@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).filter_by(password=password)
    if user.count() == 1:
        login_user(user.one())
        flash('Welcome back {0}'.format(username))
        return render_template('login.html')
    else:
        flash('Invalid login')
        return redirect(url_for('index'))

# User register handler
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username)
        if user.count() == 0:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
        
            flash('You have registered the username {0}. Please login'.format(username))
            return redirect(url_for('index'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username))
            return redirect(url_for('index'))
    # elif request.method == 'GET':
    #     pass
    else:
        abort(405)


if __name__ == '__main__':
    app.run()