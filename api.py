from flask import Flask, request, abort, url_for, render_template, session, Response
from flask import g
from flask.ext.cors import CORS
from flask_restful import Resource, Api
from passlib.hash import sha512_crypt
from corsDecorator import crossdomain
from database import DatabaseManager
from myemail import *
import json

# Config
SECRET_KEY = "development key"
# Encryption config
SECURITY_PASSWORD_SALT = 'securitykey'

app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)
api = Api(app)

# Set caching header
def response_cache_header(response, cache_control="max-age=120"):
	r = Response(response)
	r.headers['Cache-Control'] = cache_control # Two minutes by default
	return r

# Register
@app.route('/register', methods = ['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='content-type')
def register():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	password = sha512_crypt.encrypt(request.json.get('password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
	email = request.json.get('email')

	# Check if everything filled in
	if username is None or password is None or email is None:
		return abort(400) # missing arguments

	# Check if already exists
	elif db_manager.username_exists(username) or db_manager.email_exists(email):
		# username and/or email do already exist
		return response_cache_header("ERROR, username and/or email do already exist", cache_control="no-cache")
		
	else:
		db_manager.create_user(username=username, password_hash=password, email=email, email_verified=False)

		# Email verification
		token = generate_confirmation_token(email)
		confirm_url = url_for('verify_email', token=token, _external=True)
		html = render_template('email.html', confirm_url=confirm_url)
		subject = "Please confirm your email"
		send_email(email, subject, html)

		return response_cache_header("Successfully created user, please verify email.\n", cache_control="no-cache")

# Verify email
@app.route('/verify/<token>')
def verify_email(token):
	db_manager = DatabaseManager()
	email = confirm_token(token)

	if db_manager.email_is_verified(email):
		return response_cache_header("Email already verified.\n", cache_control="no-cache")
	else:
		# Verify
		db_manager.verify_email(email)
		return response_cache_header("Email Successfully verified.\n", cache_control="no-cache")

# Authenticate user
@app.route('/authenticate', methods=['POST','OPTIONS']) # Options is for the browser to validate
@crossdomain(origin='*', headers='content-type') # Headers need to be set
def authenticate():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	password = sha512_crypt.encrypt(request.json.get('password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)

	if username and password:
		if db_manager.get_user(username):
			if db_manager.get_user(username).get('email_verified'):
				# Check password
				if db_manager.check_password(username, password):
					return response_cache_header(json.dumps({
						"token": db_manager.generate_auth_token(username, password).decode("utf-8")
						}))
			else:
				return response_cache_header(json.dumps({"error":"Email not verified"}), cache_control="no-cache")
		else:
			return response_cache_header(json.dumps({"error":"User not found"}), cache_control="no-cache")
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

	# Verifiy token
	token_credentials = db_manager.verify_auth_token(token=token)
	if token_credentials is None:
		abort(401)
	elif not db_manager.check_password(token_credentials[0], token_credentials[1]):
		abort(401)
	elif token_credentials[0] != username:
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

	return response_cache_header("Saved list", cache_control="no-cache")

@app.route('/deleteList', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers='content-type')
def delete_list():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	listname = request.json.get('listname')
	token = request.json.get('token')
	
	if username == None or listname == None or token == None:
		abort(400)

	# Verifiy token
	token_credentials = db_manager.verify_auth_token(token=token)
	if token_credentials is None:
		abort(401)
	elif not db_manager.check_password(token_credentials[0], token_credentials[1]):
		abort(401)
	elif token_credentials[0] != username:
		abort(401)

	if not db_manager.listname_exists_for_user(username, listname):
		return response_cache_header("No list found", cache_control="no-cache")

	if db_manager.listname_exists_for_user(username, listname):
		db_manager.delete_list(username, listname)
		return response_cache_header("Successfully deleted list", cache_control="no-cache")

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
		if not db_manager.users_are_friends(username, friendname):
			email = db_manager.get_user(friendname).get("email")

			# Email request
			token = generate_confirmation_token([ username, friendname])
			confirm_url = url_for('accept_friend', token=token, _external=True)
			html = render_template('friend.html', confirm_url=confirm_url, name=username)
			subject = "New friend request"
			send_email(email, subject, html)

			return response_cache_header("Email sent", cache_control="no-cache")
		else:
			return response_cache_header("ERROR, already friends", cache_control="no-cache")

@app.route('/acceptFriend/<token>')
def accept_friend(token):
	db_manager = DatabaseManager()
	names = confirm_token(token)

	if db_manager.users_are_friends(names[0], names[1]):
		return response_cache_header("Already friends", cache_control="no-cache")
	else:
		db_manager.create_friendship(names[0], names[1])
		return response_cache_header("Now friends", cache_control="no-cache")

@app.route('/getFriends', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers="content-type")
def get_friends():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	token = request.json.get('token')
	
	if username == None or token == None:
		abort(400)

	# Verifiy token
	token_credentials = db_manager.verify_auth_token(token=token)
	if token_credentials is None:
		abort(401)
	elif not db_manager.check_password(token_credentials[0], token_credentials[1]):
		abort(401)
	elif token_credentials[0] != username:
		abort(401)

	friends = db_manager.get_friends_for_user(username)
	# It is unsafe to send your friends password hash to the browser... 	email_verified and id aren't needed
	for friend in friends: del friend['password_hash']; del friend['email_verified']; del friend['id']

	return response_cache_header(json.dumps({"friends":friends}))

@app.route('/changePassword', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers="content-type")
def change_password():
	db_manager = DatabaseManager()

	username = request.json.get('username')
	old_password = sha512_crypt.encrypt(request.json.get('old_password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
	new_password = sha512_crypt.encrypt(request.json.get('new_password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
	token = request.json.get('token')

	# Not everything filled in
	if username == None or old_password == None or new_password == None or token == None:
		abort(400)

	# Verifiy token
	token_credentials = db_manager.verify_auth_token(token=token)
	if token_credentials is None:
		abort(401)
	elif not db_manager.check_password(token_credentials[0], token_credentials[1]):
		abort(401)
	elif token_credentials[0] != username:
		abort(401)

	if db_manager.check_password(username, old_password):
		db_manager.change_password(username, old_password, new_password)
		return response_cache_header("Changed password", cache_control="no-cache")
	else:
		return response_cache_header("ERROR, Wrong password", cache_control="no-cache")

# REST Recource with app.route
@app.route('/<username>', methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers="content-type")
def get(username):
	db_manager = DatabaseManager()

	token = request.json.get('token')
	if token is None or token is "":
		return abort(401)
	
	# Verifiy token
	token_credentials = db_manager.verify_auth_token(token=token)
	if token_credentials is None:
		return abort(401)
	elif not db_manager.check_password(token_credentials[0], token_credentials[1]):
		return abort(401)
	
	if db_manager.username_exists(username):
		# Return all lists
		if token_credentials[0] == username:
			user_info = db_manager.get_user(username)
			list_lists = db_manager.get_lists_for_user(username)
			for l in list_lists: del l['user_id']; del l['id']

			return response_cache_header(json.dumps({
				'username': user_info.get("username"),
				'email' : user_info.get("email"),
				'lists' : list_lists
				}))
		# Return friend lists if you are friends
		elif db_manager.users_are_friends(username, token_credentials[0]):
			user_info = db_manager.get_user(username)
			list_lists = db_manager.get_lists_for_user(username)
			
			for l in list_lists[:]:  # Make a slice copy of the entire list
				if l['shared_with'] == "0":
					list_lists.remove(l)
				del l['user_id']
				del l['id']

			return response_cache_header(json.dumps({
				'username': user_info.get("username"),
				'email' : user_info.get("email"),
				'lists' : list_lists
				}))
		# Return everyone shared lists
		else:
			user_info = db_manager.get_user(username)
			list_lists = db_manager.get_lists_for_user(username)
			for l in list_lists:
				if l['shared_with'] != "2":
					list_lists.remove(l)
				del l['user_id']
				del l['id']

			return response_cache_header(json.dumps({
				'username': user_info.get("username"),
				'email' : user_info.get("email"),
				'lists' : list_lists
				}))

	else:
		return response_cache_header(json.dumps({"error":"User not found"}), cache_control="no-cache")

@app.route('/<username>/<listname>', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers="content-type")
def show_user_list(username, listname):
	db_manager = DatabaseManager()

	token = request.json.get("token")
	if token is None or token is "":
		return abort(401)
	
	# Verifiy token
	token_credentials = db_manager.verify_auth_token(token=token)
	if token_credentials is None:
		return abort(401)
	elif not db_manager.check_password(token_credentials[0], token_credentials[1]):
		return abort(401)

	if db_manager.username_exists(username):
		if db_manager.listname_exists_for_user(username, listname):
			list_data = db_manager.get_list(username, listname)
			shared_with = list_data.get("shared_with")
			translations = db_manager.get_translations_for_list(username, listname)
			for translation in translations: del translation['id']; del translation['list_id']
			
			# Check if is owner
			if username == token_credentials[0]:
				return response_cache_header(json.dumps({
					'listname' : listname,
					'language_1_tag' : list_data.get("language_1_tag"),
					'language_2_tag' : list_data.get("language_2_tag"),
					'words' : translations,
					'shared_with' : shared_with
				}))
			# Check if is friend
			elif shared_with == '1' and db_manager.users_are_friends(username, token_credentials[0]):
				return response_cache_header(json.dumps({
					'listname' : listname,
					'language_1_tag' : list_data.get("language_1_tag"),
					'language_2_tag' : list_data.get("language_2_tag"),
					'words' : translations,
					'shared_with' : shared_with
				}))
			elif shared_with == '2':
				return response_cache_header(json.dumps({
					'listname' : listname,
					'language_1_tag' : list_data.get("language_1_tag"),
					'language_2_tag' : list_data.get("language_2_tag"),
					'words' : translations,
					'shared_with' : shared_with
				}))
			else:
				abort(401)

		else:
			return response_cache_header(json.dumps({"error":"List not found"}), cache_control="no-cache")
	else:
		return response_cache_header(json.dumps({"error":"User not found"}), cache_control="no-cache")

@app.after_request
def after_request(response):
	print("after_request happening")
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
	return response

# Run app
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=False)
