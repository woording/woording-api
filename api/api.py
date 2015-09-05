from flask import Flask
from flask import g
from flask_restful import Resource, Api
import json
from corsDecorator import crossdomain

import sqlite3

# configuration
DATABASE = 'wording.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# REST Resources
class User(Resource):
	def get(self, username):
		return {
			'name': 'leon', #g.execute("select username from user")
			'lists':
				['lijst duits', 'lijst 2']
		}

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


# api.add_resource(User, '/<username>')
api.add_resource(List, '/<username>/<listname>')


#DATABASE
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# REST Recource with app.route
@app.route('/<username>')
@crossdomain(origin='*')
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
