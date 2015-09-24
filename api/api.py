from flask import Flask, request, abort, url_for, render_template, session, Response
from flask import g
from flask_restful import Resource, Api
from flask_mail import Mail
from passlib.hash import sha512_crypt
import json
from corsDecorator import crossdomain
from database import DatabaseManager
from myemail import *

# Config
SECRET_KEY = "development key"
# Encryption config
SECURITY_PASSWORD_SALT = 'securitykey'
# Email config
MAIL_SERVER = "smtp.gmail.com" # SMTP Server
MAIL_PORT = 465 # SMTP Port
MAIL_USE_TLS = False
MAIL_USE_SSL = True

MAIL_DEBUG = True
# Login information
MAIL_USERNAME = "noreply.wording@gmail.com"
MAIL_PASSWORD = "TestingPassword"
# Mail sender addres
MAIL_DEFAULT_SENDER = "noreply.wording@gmail.com"

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)

# Setup email
mail = Mail(app)

# Register
@app.route('/register', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='content-type')
def register():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	password = sha512_crypt.encrypt(request.json.get('password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
	email = request.json.get('email')

	if username is None or password is None or email is None:
		return "ERROR, not everything filled in" # missing arguments
	elif db_manager.username_exists(username) or db_manager.email_exists(email):
		return "ERROR, username and/or email do already exist" # username and/or email do already exist
	else:
		db_manager.create_user(username=username, password_hash=password, email=email, email_verified=False)

		# Email verification
		token = generate_confirmation_token(email)
		confirm_url = url_for('verify_email', token=token, _external=True)
		html = render_template('email.html', confirm_url=confirm_url)
		subject = "Please confirm your email"
		send_email(email, subject, html)

		return "Successfully created user, please verify email.\n"

# Verify email
@app.route('/verify/<token>')
def verify_email(token):
	db_manager = DatabaseManager()
	email = confirm_token(token)

	if db_manager.email_is_verified(email):
		return "Email already verified.\n"
	else:
		db_manager.verify_email(email)
		return "Email Successfully verified.\n"

@app.route('/authenticate', methods=['POST','OPTIONS']) # Options is for the browser to validate
@crossdomain(origin='*', headers='content-type') # Headers need to be set
def authenticate():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	password = sha512_crypt.encrypt(request.json.get('password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)

	if username and password:
		if db_manager.get_user(username).get('email_verified'):
			if db_manager.check_password(username, password):
				return json.dumps({
					"token": db_manager.generate_auth_token(username).decode("utf-8"),
					"friends": db_manager.get_user(username).get("friends")
					})
		else:
			return "ERROR, Email not verified"
	else:
		return Response('Login!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})

# Save list
@app.route('/savelist', methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers="content-type")
def save_list():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	list_data = request.json.get('list_data')
	token = request.json.get('token')

	if username == None or list_data == None or token == None:
		abort(400)

	token_username = db_manager.verify_auth_token(token=token)
	if token_username == None or token_username != username:
		abort(401)

	if list_data.get('listname') is None or list_data.get('language_1_tag') is None or list_data.get('language_2_tag') is None or list_data.get('shared_with') is None:
		abort(400)

	if list_data.get('listname') is "" or list_data.get('language_1_tag') is "" or list_data.get('language_2_tag') is "" or list_data.get('shared_with') is "":
		abort(400)

	if db_manager.listname_exists_for_user(username, list_data.get('listname')):
		db_manager.delete_list(username, list_data.get('listname'))

	db_manager.create_list(username, list_data.get('listname'), list_data.get('language_1_tag'), list_data.get('language_2_tag'), list_data.get('shared_with'))
	words = list_data.get('words')
	
	for i in range(len(words)):
		word = words[i]
		if word.get('language_1_text') is u'' or word.get('language_2_text') is u'':
			continue
		db_manager.create_translation(username, list_data.get('listname'), word.get('language_1_text'), word.get('language_2_text'))

	return "Saved list"

@app.route('/deleteList', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='content-type')
def delete_list():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	listname = request.json.get('listname')
	token = request.json.get('token')
	
	if username == None or listname == None or token == None:
		abort(400)

	token_username = db_manager.verify_auth_token(token=token)
	if token_username == None or token_username != username:
		abort(401)

	if not db_manager.listname_exists_for_user(username, listname):
		return "No list found"

	if db_manager.listname_exists_for_user(username, listname):
		db_manager.delete_list(username, listname)
		return "Successfully deleted list"

	return abort(401)

# Friends
@app.route('/friendRequest', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='content-type')
def friend_request():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	friendname = request.json.get('friendname')

	if username == None or friendname == None:
		abort(400)

	if db_manager.username_exists(username) and db_manager.username_exists(friendname):
		email = db_manager.get_user(friendname).get("email")

		# Email request
		token = generate_confirmation_token([ username, friendname])
		confirm_url = url_for('accept_friend', token=token, _external=True)
		html = render_template('friend.html', confirm_url=confirm_url, name=username)
		subject = "New friend request"
		send_email(email, subject, html)

		return "Email sent"

@app.route('/acceptFriend/<token>')
def accept_friend(token):
	db_manager = DatabaseManager()
	names = confirm_token(token)

	if db_manager.are_friends(names[0], names[1]):
		return "Already friends"
	else:
		db_manager.add_friend(names[0], names[1])
		db_manager.add_friend(names[1], names[0])
		return "Now friends"


# REST Recource with app.route
@app.route('/<username>', methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers="content-type")
def get(username):
	db_manager = DatabaseManager()

	token = request.json.get('token')
	if token is None or token is "":
		return json.dumps({ 'username':'ERROR, No token' })
	
	token_username = db_manager.verify_auth_token(token=token)
	if token_username is None:
		return json.dumps({ 'username':'ERROR, No user' })
	
	if db_manager.username_exists(username):
		if token_username == username: # Need to do something with shared lists...
			user_info = db_manager.get_user(username)
			list_lists = db_manager.get_lists_for_user(username)
			for l in list_lists: del l['user_id']; del l['id']

			return json.dumps({
				'username': user_info.get("username"),
				'email' : user_info.get("email"),
				'lists' : list_lists
				})
		elif db_manager.are_friends(username, token_username):
			user_info = db_manager.get_user(username)
			list_lists = db_manager.get_lists_for_user(username)
			for l in list_lists:
				if l['shared_with'] == "0":
					list_lists.remove(l)
				del l['user_id']
				del l['id']

			return json.dumps({
				'username': user_info.get("username"),
				'email' : user_info.get("email"),
				'lists' : list_lists
				})
		else:
			user_info = db_manager.get_user(username)
			list_lists = db_manager.get_lists_for_user(username)
			for l in list_lists:
				if l['shared_with'] != "2":
					list_lists.remove(l)
				del l['user_id']
				del l['id']

			return json.dumps({
				'username': user_info.get("username"),
				'email' : user_info.get("email"),
				'lists' : list_lists
				})

	else:
		return json.dumps({
			'username': 'ERROR: This shouldn\'t happen'
			})

@app.route('/<username>/<listname>', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers="content-type")
def show_user_list(username, listname):
	db_manager = DatabaseManager()

	token = request.json.get("token")
	if token is None or token is "":
		return json.dumps({ 'username':'ERROR, No token' })
	
	token_username = db_manager.verify_auth_token(token=token)
	if token_username is None:
		return json.dumps({ 'username':'ERROR, No user' })

	if db_manager.username_exists(username):
		if db_manager.listname_exists_for_user(username, listname):
			list_data = db_manager.get_list(username, listname)
			shared_with = list_data.get("shared_with")
			translations = db_manager.get_translations_for_list(username, listname)
			for translation in translations: del translation['id']; del translation['list_id']
			
			# Check if is owner
			if username == token_username:
				return json.dumps({
					'listname' : listname,
					'language_1_tag' : list_data.get("language_1_tag"),
					'language_2_tag' : list_data.get("language_2_tag"),
					'words' : translations,
					'shared_with' : shared_with
				})
			elif shared_with == '1' and db_manager.are_friends(username, token_username): # and isFriend()
				return json.dumps({
					'listname' : listname,
					'language_1_tag' : list_data.get("language_1_tag"),
					'language_2_tag' : list_data.get("language_2_tag"),
					'words' : translations,
					'shared_with' : shared_with
				})
			elif shared_with == '2':
				return json.dumps({
					'listname' : listname,
					'language_1_tag' : list_data.get("language_1_tag"),
					'language_2_tag' : list_data.get("language_2_tag"),
					'words' : translations,
					'shared_with' : shared_with
				})
			else:
				abort(401)

		else:
			return json.dumps({
				'username': 'ERROR: This shouldn\'t happen'
				})
	else:
		return json.dumps({
			'username': 'ERROR: This shouldn\'t happen'
			})


# Run app
if __name__ == '__main__':
	app.run('127.0.0.1', debug=True)
