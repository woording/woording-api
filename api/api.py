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

# REST Resources
class User(Resource):

	def get(self, username):

		db_manager = DatabaseManager()

		if db_manager.username_exists(username):

			user_info = db_manager.get_user(username)
			list_lists = db_manager.get_lists_for_user(username)
			for l in list_lists: del l['user_id']; del l['id']

			return json.dumps({
				'username': user_info.get("username"),
				'email' : user_info.get("email"),
				'lists' : list_lists
				})

		else:
			print ('ERROR: User does not exists')


class List(Resource):
	def get(self, username, listname):

		db_manager = DatabaseManager()

		if db_manager.username_exists(username):

			if db_manager.listname_exists_for_user(username, listname):

				list_data = db_manager.get_list(username, listname)
				translations = db_manager.get_translations_for_list(username, listname)

				for translation in translations: del translation['id']; del translation['list_id']

				return json.dumps({
					'listname' : listname,
					'language_1_tag' : list_data.get("language_1_tag"),
					'language_2_tag' : list_data.get("language_2_tag"),

					'words' : translations
					})

			else:
				print("ERROR, List doesn't exist")

		else:
			print("ERROR, User doesn't exists")


# api.add_resource(User, '/<username>')
# api.add_resource(List, '/<username>/<listname>')

# Register
@app.route('/register', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='content-type')
def register():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	password = sha512_crypt.encrypt(request.json.get('password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
	email = request.json.get('email')

	if username is None or password is None or email is None:
		return abort(400) # missing arguments
	elif db_manager.username_exists(username) or db_manager.email_exists(email):
		return abort(400) # username and/or email do already exist
	else:
		db_manager.create_user(username=username, password_hash=password, email=email, email_verified=False)

		# Email verification
		token = generate_confirmation_token(email)
		confirm_url = url_for('verify_email', token=token, _external=True)
		html = render_template('email.html', confirm_url=confirm_url)
		subject = "Please confirm your email"
		send_email(email, subject, html)
		print("Email send")

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

	if username and password and db_manager.check_password(username, password):
		return db_manager.generate_auth_token(username)
	else:
		return Response('Login!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})

# Save list
@app.route('/savelist', methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers="content-type")
def save_list():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	list_data = request.json.get('list_data')
	
	print(username)
	print(list_data)

	if username is None or list_data is None:
		abort(400)

	db_manager.create_list(username, list_data.get('listname'), list_data.get('language_1_tag'), list_data.get('language_2_tag'))
	words = list_data.get('words')

	for i in words:
		db_manager.create_translation(username, list_data.get('listname'), word.get('language_1_text'), word.get('language_2_text'))

	return "Saved list"

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
	
	if db_manager.username_exists(username) and token_username == username: # Need to do something with shared lists...
		user_info = db_manager.get_user(username)
		list_lists = db_manager.get_lists_for_user(username)
		for l in list_lists: del l['user_id']; del l['id']

		return json.dumps({
			'username': user_info.get("username"),
			'email' : user_info.get("email"),
			'lists' : list_lists
			})
	else:
		return json.dumps({
			'username': 'ERROR: This shouldn\'t happen'
			})

@app.route('/<username>/<listname>')
@crossdomain(origin='*')
def show_user_list(username, listname):
	db_manager = DatabaseManager()

	if db_manager.username_exists(username):
		if db_manager.listname_exists_for_user(username, listname):
			list_data = db_manager.get_list(username, listname)
			translations = db_manager.get_translations_for_list(username, listname)
			for translation in translations: del translation['id']; del translation['list_id']
			return json.dumps({
				'listname' : listname,
				'language_1_tag' : list_data.get("language_1_tag"),
				'language_2_tag' : list_data.get("language_2_tag"),
				'words' : translations
				})
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
