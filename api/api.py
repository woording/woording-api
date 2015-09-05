from flask import Flask
from flask import g
from flask_restful import Resource, Api
import json
from corsDecorator import crossdomain
from database import DatabaseManager

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)



# REST Resources
class User(Resource):
	def get(self, username):

		db_manager = DatabaseManager()
		if db_manager.username_exists(username):

			user_info = db_manager.get_user_info(username)

			return {
				'username': user_info.get("username"),
				'email' : user_info.get("email"),
				'email_verified' : user_info.get("email_verified"),
				'password_hash' : user_info.get("password_hash")
			}
		else:
			print ('ERROR: User does not exists')


class List(Resource):
	def get(self, username, listname):
		return {
			'name': listname,
			'languages': {
				'language-1' : 'Nederlands',
				'language-2' : 'Engels'
			},
			'words': [
				{
					'language-1' : 'auto',
					'language-2' : 'car'
				},
				{
					'language-1' : 'boom',
					'language-2' : 'tree'
				}
			]

		}


api.add_resource(User, '/<username>')
api.add_resource(List, '/<username>/<listname>')



# REST Recource with app.route
@app.route('/<username>')
# @crossdomain(origin='*')
def show_user_profile(username):
    return json.dumps({
			'name': username, #g.execute("select username from user")
			'lists':
				['lijst duits', 'lijst 2']
		})

# @app.route('/<username>/<list>')
# def show_user_list(username, list):
# 	return 'Show list ' + username + '/' + list

# @app.route('/about')
# def show_about():
# 	return 'Insert about page here'


# Run app
if __name__ == '__main__':
	app.run('127.0.0.1', debug=True)
