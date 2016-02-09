from flask import Flask, request, abort, url_for, render_template, session, Response, redirect
from flask import g
from flask.ext.cors import CORS, cross_origin
from flask_restful import Resource, Api
from passlib.hash import sha512_crypt
from database import DatabaseManager
from myemail import *
from validate_email import validate_email
import time
import time
import ssl
import json
from urllib.request import urlopen

# Config
SECRET_KEY = "development key"
# Encryption config
SECURITY_PASSWORD_SALT = 'securitykey'

app = Flask(__name__)

CORS(app)
app.config.from_object(__name__)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Set caching header
def response_cache_header(response, cache_control="max-age=120"):
	r = Response(response)
	r.headers['Cache-Control'] = cache_control # Two minutes by default
	return r

@app.route('/')
def redirect_homepage():
    return redirect("https://woording.com")


# Register
@app.route('/register', methods = ['POST'])
def register():
        db_manager = DatabaseManager()

        username = request.json.get('username')
        password = sha512_crypt.encrypt(request.json.get('password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
        email = request.json.get('email')

        email = email.lower()

        if not validate_email(email):
                return response_cache_header(json.dumps({"response":"Not a valid email address", "success": False}), cache_control="no-cache")

	# Check if everything filled in
        elif username is None or password is None or email is None:
                return abort(400) # missing arguments

	# Check if already exists
        elif db_manager.username_exists(username) or db_manager.email_exists(email):
		# username and/or email do already exist
                return response_cache_header(json.dumps({"response":"ERROR, username and/or email already exist", "success": False}), cache_control="no-cache")

        else:
                db_manager.create_user(username=username, password_hash=password, email=email, email_verified=False)

                # Email verification
                token = generate_confirmation_token(email)
                confirm_url = 'https://api.woording.com/verify/' + token
                html = render_template('email.html', confirm_url=confirm_url)
                subject = "Please confirm your email"
                send_email(email, subject, html)

                return response_cache_header(json.dumps({"response":"Succesfully created user, please verify email.", "success": True}), cache_control="no-cache")

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
@app.route('/authenticate', methods=['POST'])
def authenticate():
        db_manager = DatabaseManager()

        username = request.json.get('username')
        password = sha512_crypt.encrypt(request.json.get('password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)

        if username and password:
                if db_manager.get_user(username):
                        if db_manager.get_user(username).get('email_verified'):
                                # Check password
                                if db_manager.check_password(username, password):
                                        token = db_manager.generate_auth_token(username.lower(), password).decode("utf-8")
                                        print(token)
                                        return response_cache_header(json.dumps({
                                                "token": token,
                                                "success": True
                                        }))
                                else:
                                    return response_cache_header(json.dumps({"error":"Incorrect password and/or username", "success":False}), cache_control="no-cache")
                        else:
                            return response_cache_header(json.dumps({"error":"Email not verified", "success":False}), cache_control="no-cache")
                else:
                    return response_cache_header(json.dumps({"error":"User does not exist", "success":False}), cache_control="no-cache")
        else:
                return Response('Login!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})

# Validate Captcha
@app.route('/validateCaptcha', methods=['POST'])
def validate():
    url = request.json.get('url')
    if url == None:
        abort(400)
    else:
        response = urlopen(url)
        data = response.read()
        success = json.loads(data.decode('utf-8'))['success']

        return response_cache_header(json.dumps({'answer':success}), cache_control="no-cache")

# Save list
@app.route('/savelist', methods=['POST'])
def save_list():
        db_manager = DatabaseManager()

        username = request.json.get('username').lower()
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
                old_list = db_manager.get_list(username, list_data['listname'])
                old_words = db_manager.get_translations_for_list(username, list_data['listname'])
                db_manager.delete_list(username, list_data.get('listname'))
                db_manager.create_list(username, list_data.get('listname'), list_data.get('language_1_tag'), list_data.get('language_2_tag'), list_data.get('shared_with'))
                words = list_data.get('words')

                for i in range(len(words)):
                        word = words[i]
                        if word.get('language_1_text') is u'' or word.get('language_2_text') is u'':
                                continue
                        db_manager.create_translation(username, list_data.get('listname'), word.get('language_1_text'), word.get('language_2_text'))

                return response_cache_header(json.dumps( { 'response' : 'List exists', 'old_list':old_list, 'old_words':old_words } ), cache_control="no-cache")

        db_manager.create_list(username, list_data.get('listname'), list_data.get('language_1_tag'), list_data.get('language_2_tag'), list_data.get('shared_with'))
        words = list_data.get('words')

        totaltimeStart = int(round(time.time() * 1000))
        print(words)
        db_manager.add_translations(username, words, list_data.get('listname'))

        for i in range(len(words)):
                word = words[i]
                if word.get('language_1_text') is u'' or word.get('language_2_text') is u'':
                        continue
                db_manager.create_translation(username, list_data.get('listname'), word.get('language_1_text'), word.get('language_2_text'))

        totaltimeEnd = int(round(time.time() * 1000))
        print("Takes: " + str(totaltimeEnd - totaltimeStart) + " milliseconds")

        return response_cache_header(json.dumps( { 'response' : 'Saved list!' } ), cache_control="no-cache")

@app.route('/deleteList', methods=['POST'])
def delete_list():
	db_manager = DatabaseManager()

	username = request.json.get('username').lower()
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
		return response_cache_header(json.dumps( { 'response':'Successfully deleted list' } ), cache_control="no-cache")

	return abort(401)

# Friends
@app.route('/friendRequest', methods=['POST'])
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

@app.route('/getFriends', methods=['POST'])
def get_friends():
	db_manager = DatabaseManager()

	username = request.json.get('username').lower()
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

@app.route('/changePassword', methods=['POST'])
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
@app.route('/<username>', methods=["POST"])
def get(username):
        db_manager = DatabaseManager()
        username = username.lower()

        token = request.json.get('token')
        if token is None or token is "":
                print('No token')
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
                        for l in list_lists[:]:  # Make a slice copy of the entire list
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
                return response_cache_header(json.dumps({"error":"User not found" + username}), cache_control="no-cache")

@app.route('/<username>/<listname>', methods=['POST'])
def show_user_list(username, listname):
        db_manager = DatabaseManager()
        username = username.lower()

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

# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('apicert.crt', 'apikey.key')

# # Run app
# if __name__ == '__main__':
        # app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=context)

# Run app no ssl
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
