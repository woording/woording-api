from flask import Flask, request, session, render_template, abort, redirect, url_for, flash
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from passlib.hash import sha512_crypt
from datetime import datetime
import os

# Flask config
DEBUG = True
SECRET_KEY = 'development key'
# Database config
SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
# Encryption config
SECURITY_PASSWORD_SALT = 'securitykey'
# Email config
MAIL_SERVER = "localhost" # SMTP Server
MAIL_PORT = 587 # SMTP Port
MAIL_USE_TLS = True
MAIL_USE_SSL = False

MAIL_DEBUG = DEBUG
# Login information
MAIL_USERNAME = None
MAIL_PASSWORD = None
# Mail sender addres
MAIL_DEFAULT_SENDER = None


app = Flask(__name__)
app.config.from_object(__name__)

# Init login manager
login_manager = LoginManager()
login_manager.init_app(app)
# Init database
db = SQLAlchemy(app)
# Init mail
mail = Mail(app)

# Database class
class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String())
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        self.confirmed = True
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.id)
 
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
    password = sha512_crypt.encrypt(request.form['password'], salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
    
    user = User.query.filter_by(username=username).filter_by(password=password)
    if user.count() == 1:
        if User.query.filter_by(username=username).filter_by(password=password).filter_by(confirmed=True).count() == 1:
            login_user(user.one())
            flash('Welcome back {0}'.format(username), 'success')
            return render_template('login.html')
        else:
            flash("Your email has to be confirmed before loggin in.", 'error')
            return redirect(url_for('index'))
    else:
        flash('Invalid login', 'error')
        return redirect(url_for('index'))

# User register handler
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = sha512_crypt.encrypt(request.form['password'], salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
        email = request.form['email']

        if password == '':
            flash('You have to type a password', 'error')
            return redirect(url_for('index'))
        
        user = User.query.filter_by(username=username)
        if user.count() == 0:
            if User.query.filter_by(email=email).count() == 0:
                user = User(username=username, password=password, email=email)
                db.session.add(user)
                db.session.commit()

                # token = generate_confirmation_token(email)
                # confirm_url = url_for('confirm_email', token=token, _external=True)
                # template = render_template('email_confirmation.html', confirm_url=confirm_url)
                # subject = "Please confirm your email"
                # send_email(email, subject, template)

                flash('You have registered the username {0}. Please verify your email.'.format(username), 'success')
                return redirect(url_for('index'))
            else:
                flash('This email adress is already in use, please try another.', 'error')
                return redirect(url_for('index'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username), 'error')
            return redirect(url_for('index'))
    else:
        abort(405)


# Email verification token
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients = [to],
        html = template,
        sender = app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt = app.config['SECURITY_PASSWORD_SALT'],
            max_age =expiration
        )
    except:
        return False
    return email

# Confirmation link
@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
    
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))

# Run app
if __name__ == '__main__':
    app.run()
