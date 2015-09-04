from flask import Flask, request, session, render_template, abort, redirect, url_for, flash
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
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
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(20))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

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
        flash('Welcome back {0}'.format(username), 'succes')
        return render_template('login.html')
    else:
        flash('Invalid login', 'error')
        return redirect(url_for('index'))

# User register handler
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if password == '':
            flash('You have to type a password', 'error')
            return redirect(url_for('index'))
        
        user = User.query.filter_by(username=username)
        if user.count() == 0:
            user = User(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
        
            flash('You have registered the username {0}. Please login'.format(username), 'succes')
            return redirect(url_for('index'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username), 'error')
            return redirect(url_for('index'))
    else:
        abort(405)


if __name__ == '__main__':
    app.run()