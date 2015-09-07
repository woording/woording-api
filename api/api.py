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



# REST Recource with app.route
@app.route('/<username>')
@crossdomain(origin='*')
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





# @app.route('/about')
# def show_about():
# 	return 'Insert about page here'


# Run app
if __name__ == '__main__':
	app.run('127.0.0.1', debug=True)
