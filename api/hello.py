from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class User(Resource):
	def get(self, username):
		return {'name': username, 'lists': ['lijst duits', 'lijst 2']}

class List(Resource):
	def get(self, username, listname):
		return {'name': listname, 'languages': {'language_1' : 'Nederlands', 'language_2' : 'Engels'}, 'words': [{'language_1' : 'auto', 'language_2' : 'car'}, {'language_1' : 'boom', 'language_2' : 'tree'}]}



api.add_resource(User, '/<username>')
api.add_resource(List, '/<username>/<listname>')


# @app.route('/<username>')
# def show_user_profile(username):
# 	return 'Hello ' + username

# @app.route('/<username>/<list>')
# def show_user_list(username, list):
# 	return 'Show list ' + username + '/' + list 

# @app.route('/about')
# def show_about():
# 	return 'Insert about page here'

if __name__ == '__main__':
	app.run('0.0.0.0', debug=True)