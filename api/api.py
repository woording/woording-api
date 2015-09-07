from flask import Flask, request
from flask import g
from flask_restful import Resource, Api
from flask.ext.httpauth import HTTPBasicAuth
from passlib.hash import sha512_crypt
import json
from corsDecorator import crossdomain
from database import DatabaseManager

# Config
# Encryption config
SECURITY_PASSWORD_SALT = 'securitykey'

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)

# HTTP Authentication
auth = HTTPBasicAuth()

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
api.add_resource(List, '/<username>/<listname>')



# REST Recource with app.route
@app.route('/<username>')
@crossdomain(origin='*')
@auth.login_required
def get(username):

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
        return json.dumps({
            'username': 'ERROR: This shouldn\'t happen'
            })

# @app.route('/<username>/<list>')
# def show_user_list(username, list):
# 	return 'Show list ' + username + '/' + list

# @app.route('/about')
# def show_about():
# 	return 'Insert about page here'


# Verify password
@auth.verify_password
def verify_password(username, password):
	db_manager = DatabaseManager()

	password_hash = sha512_crypt.encrypt(password, salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)

	user = db_manager.get_user(username)

	if not user or not db_manager.check_password(username, password):
		return False
	
	g.user = user
	return True

# Login
# @app.route('/login', methods = ['POST'])
# def login():
# 	username = request.json.get('username')
#     password = sha512_crypt.encrypt(request.json.get('password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
#     if username is None or password is None:
#         abort(400) # missing arguments
#     user = db_manager.get_user(username)

#     valid_login = db_manager.check_password(username=username, password=password)

#     if valid_login:
#     	return "Successfully logged in"

# Register
@app.route('/register', methods = ['POST'])
def register():
	db_manager = DatabaseManager()
	
	username = request.json.get('username')
	password = sha512_crypt.encrypt(request.json.get('password'), salt=app.config['SECURITY_PASSWORD_SALT'], rounds=5000)
	email = request.json.get('email')
	if username is None or password is None or email is None:
		abort(400) # missing arguments
	if db_manager.username_exists(username) is not False or db_manager.email_exists(email) is not False:
		abort(400)

	db_manager.create_user(username=username, password_hash=password, email=email, email_verified=False)

    # TODO Create email verification



# Run app
if __name__ == '__main__':
	app.run('127.0.0.1', debug=True)
