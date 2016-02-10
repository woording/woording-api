import sqlite3, json
import time
from itsdangerous import (JSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

SECRET_KEY = "SECRET"

# A class that makes connecting to the database safe and easy
class DatabaseConnection(object):
	def __init__(self, db):
		# Create a database connection when initializing
		self.conn = sqlite3.connect(db)
		# Enable foreign_keys for extra safety
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()

	def query(self, arg):
                self.cur.execute(arg)
                self.conn.commit()
                return self.cur

	def __del__(self):
		# Close the database connection when done
		self.conn.close()


# A class that contains functions for
# interacting with the database
class DatabaseManager(object):

	def __init__(self):
		self.database_path = 'wording.db'

	# Token
	def generate_auth_token(self, username, password, expiration = 0):
		s = Serializer(SECRET_KEY)
		return s.dumps({ 'username': username, 'password': password })

	# Verify token
	def verify_auth_token(self, token):
		s = Serializer(SECRET_KEY)
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		return [data['username'], data['password']]

	# Create a user database record
	def create_user(self, username, email, email_verified, password_hash):

		# Check if the username is available
		if not self.username_exists(username):

			# Create a DatabaseConnection
			db_conn = DatabaseConnection(self.database_path)

			# Genereate the query
			query_text = 'INSERT INTO user (username, email, email_verified, password_hash) VALUES ("' + username + '", "' + email + '", "' + str(int(email_verified)) + '", "' + password_hash + '")'

			# Use the query to create a new user
			db_conn.query(query_text)

		else:
			# TODO Handle username is not available error
			print ('ERROR: Username is not available')

	# Create a list database record
	# A list is tied to a user, so the username must exist
	def create_list(self, username, listname, language_1_tag, language_2_tag, shared_with):

		# Check if user exists
		if self.username_exists(username):

			# Check if the listname is available
			if not self.listname_exists_for_user(username, listname):

				user_id = self.get_user(username).get("id")

				# Generate the query
				query_text = 'INSERT INTO list (user_id, listname, language_1_tag, language_2_tag, shared) VALUES (' + str(user_id) + ', "' + listname + '", "' + language_1_tag + '", "' + language_2_tag + '", "' + shared_with + '")'

				# Use the query to create a new list

				#Create a DatabaseConnection
				db_conn = DatabaseConnection(self.database_path)
				db_conn.query(query_text)
			else:
				print ('ERROR: Listname already exists for user')

		else:
			print ('ERROR: User does not exist')

	# Create a translation database record
	# A translation is tied to a list, and a list is tied to a user
	# so both the username and listname must exist.
	def create_translation(self, username, listname, language_1_text, language_2_text):


                # Check if user exists
                if self.username_exists(username):

                        # Check if list exists
                        if self.listname_exists_for_user(username, listname):

                                db_conn = DatabaseConnection(self.database_path)

                                list_id = self.get_list(username, listname).get("id")

                                query_text = 'INSERT INTO translation (list_id, language_1_text, language_2_text) VALUES (' + str(list_id) + ', "' + language_1_text + '", "' + language_2_text + '")'

                                db_conn.query(query_text)
                        else:
                                print('ERROR: List does not exist')

                else:
                        print('ERROR: User does not exist')

	def delete_list(self, username, listname):
		if self.username_exists(username):
			if (self.listname_exists_for_user(username, listname)):

				db_conn = DatabaseConnection(self.database_path);
				list_id = self.get_list(username, listname).get("id")

				# Delete list
				query_text = 'DELETE FROM list WHERE id = ' + str(list_id)
				db_conn.query(query_text)

			else:
				print('ERROR: List does not exist')

		else:
			print('ERROR: User does not exist')	

	def add_auth_token(self, selector, token, user_id):
            db_conn = DatabaseConnection(self.database_path)
            
            query_text = 'INSERT INTO auth_tokens (selector, token, user_id, expires) VALUES ("' + selector + '", "' + token + '", ' + str(user_id) + ', + "' + "2037" + '")'
            db_conn.query(query_text)

	def get_auth_id(self, selector):
            db_conn = DatabaseConnection(self.database_path)

            query_text = 'SELECT user_id, token FROM auth_tokens WHERE selector=selector'

            if db_conn.query(query_text).fetchone() is not None:

                user_id = db_conn.query(query_text).fetchone()[0]
                token = db_conn.query(query_text).fetchone()[1]

                query_text = 'SELECT username FROM user WHERE id=' + str(user_id)

                username = db_conn.query(query_text).fetchone()[0]

                query_text = 'SELECT id FROM auth_tokens WHERE selector = ' + "'" + str(selector) + "'"

                query_text = 'DELETE FROM auth_tokens WHERE selector = ' + "'" + str(selector) + "'"
                print(query_text)

                db_conn.query(query_text)

                return json.dumps({'username':username, 'token':token})

            else:
                return False

            
	# Get all user data from a database record by username
	def get_user(self, username): 

		# Check if the user exists
		if self.username_exists(username):

                        # Create a DatabaseConnection
                        db_conn = DatabaseConnection(self.database_path)

                        # Generate the query
                        query_text = 'SELECT * FROM user WHERE LOWER(username) = "' + username.lower() + '"'

                        # Fetch the first record
                        user_record = db_conn.query(query_text).fetchone()

                        # Create a dictionary from the user_info and return it
                        return self.get_dictionary_from_user_record(user_record)

		else:
			print ('ERROR: User does not exist')

	def get_username(self, user_id):

		if self.user_id_exists(user_id):
			db_conn = DatabaseConnection(self.database_path)

			query_text = 'SELECT username FROM user WHERE id = "' + str(user_id) + '"'

			username = db_conn.query(query_text).fetchone()
			
			return username[0]

	def user_id_exists(self, user_id):
		return user_id in self.get_user_id_list()

	def get_user_id_list(self):
		# Create a DatabaseConnection
 		db_conn = DatabaseConnection(self.database_path)
 
 		# Get all the username rows
 		user_id_rows = db_conn.query('SELECT id FROM user').fetchall()
 
 		# Extract the first item
 		user_ids = tuple(user_id[0] for user_id in user_id_rows)
 		
 		return user_ids

 	# Check if the password is correct
	def check_password(self, username, password):

		# Check if the user does exist
		if self.username_exists(username):
			# Create database connection
			db_conn = DatabaseConnection(self.database_path)

			query_text = 'SELECT * FROM user WHERE LOWER(username) = "' + username.lower() + '" AND password_hash = "' + password + '"'

			user = db_conn.query(query_text).fetchone();

			return user is not None

	# Change the password of a user
	def change_password(self, username, old_password, new_password):
		# Check if the user does exist
		if self.username_exists(username):
			# Check if the old password isn't wrong
			if self.check_password(username, old_password):
				db_conn = DatabaseConnection(self.database_path)

				query_text = 'UPDATE user SET password_hash = "' + new_password + '" WHERE username = "' + username + '" AND password_hash = "' + old_password + '"'
				db_conn.query(query_text)

	def verify_email(self, email_to_verify):
		if self.email_is_verified(email_to_verify):
			print('Email already verified')
		else:

			db_conn = DatabaseConnection(self.database_path)

			query_text = 'UPDATE user SET email_verified = 1 WHERE email = "' + email_to_verify + '"'

			db_conn.query(query_text)
		
	# Check if a email address is verified, returns a Boolean
	def email_is_verified(self, email_to_check):

		db_conn = DatabaseConnection(self.database_path)

		if self.email_exists(email_to_check):
			record = db_conn.query('SELECT email_verified FROM user WHERE email = "' + email_to_check + '"').fetchone()

			return record[0] is 1

		else:
			return False

	def username_exists(self, username):

		# If the username is in the username list, it exists
                usernames = [x.lower() for x in self.get_username_list()]
                return username.lower() in usernames
		# return username in self.get_username_list()

	def email_exists(self, email):
		return email in self.get_email_list()

	def listname_exists_for_user(self, username, listname):

		# If the listname is in the user's list of lists, it exiss
		return listname in self.get_listnames_for_user(username)


	def get_friend_ids_for_user(self, username):

		# Set up the database connection and get the user_id for username
		db_conn = DatabaseConnection(self.database_path)
		user_id = self.get_user(username).get("id")

		# Both user_1_id and user_2_id can match our user_id, so we'll have to do two queries
		friend_id_rows_part1 = db_conn.query('SELECT user_1_id FROM friendship WHERE user_2_id = "' + str(user_id) + '"').fetchall()
		friend_id_rows_part2 = db_conn.query('SELECT user_2_id FROM friendship WHERE user_1_id = "' + str(user_id) + '"').fetchall()

		# Join the retrieved parts in one array
		friend_id_rows = friend_id_rows_part1 + friend_id_rows_part2

		# Extract the first item
		friend_ids = tuple(friend_id[0] for friend_id in friend_id_rows)

		return friend_ids

	# Check if users are already friends
	def users_are_friends(self, username_1, username_2):

		user_1_friend_ids = self.get_friend_ids_for_user(username_1)
		user_2_id = self.get_user(username_2).get("id")

		return user_2_id in user_1_friend_ids

	# Get all users friends
	def get_friends_for_user(self, username):

		# TODO: Sanity checks

		# get all friend id's
		friend_ids = self.get_friend_ids_for_user(username)

		# Map the results of get_username and firend_ids on friends_usernames
		friend_usernames = list(map(self.get_username, friend_ids))

		# Map the results of get_user and friend_usernames on friends
		friends = list(map(self.get_user, friend_usernames))

		return friends

	# Create a friendship between users
	def create_friendship(self, username_1, username_2):

		# TODO: Sanity checks

		user_1_id = self.get_user(username_1).get("id")
		user_2_id = self.get_user(username_2).get("id")

		if not self.users_are_friends(username_1, username_2):

			db_conn = DatabaseConnection(self.database_path)
			db_conn.query("INSERT into friendship (user_1_id, user_2_id) VALUES (" + str(user_1_id) + ", " + str(user_2_id) + ")")


	def get_username_list(self):

                # Create a DatabaseConnection
                db_conn = DatabaseConnection(self.database_path)

                # Get all the username rows
                username_rows = db_conn.query('SELECT username FROM user').fetchall()
                # Extract the first item
                usernames = tuple(username[0] for username in username_rows)
                
                return usernames

	def get_email_list(self):
		# Create a DatabaseConnection
		db_conn = DatabaseConnection(self.database_path)

		# Get all email rows
		email_rows = db_conn.query('SELECT email FROM user').fetchall()

		emails = tuple(email[0] for email in email_rows)

		return emails

	def get_listnames_for_user(self, username):

		# function to get listname from list dictionary
		def get_listname(list_dictionary):
			return list_dictionary.get('listname')

		# Map the function on every list dictionary
		listnames = list(map(get_listname, self.get_lists_for_user(username)))

		return listnames

	# Get all the lists for a user
	def get_lists_for_user(self, username):
		db_conn = DatabaseConnection(self.database_path)

		user_id = self.get_user(username).get("id")

		# Get all list rows
		list_rows = db_conn.query('SELECT * FROM list WHERE user_id = "' + str(user_id) + '"').fetchall()

		# Map the results of dictionary_from_list on list_dictionaries
		list_dictionaries = list(map(self.get_dictionary_from_list_record, list_rows))

		return list_dictionaries

	def get_list(self, username, listname):

		# Check if user exists
		if self.username_exists(username):

			# Check if list exists
			if self.listname_exists_for_user(username, listname):

				user_id = self.get_user(username).get("id");

				db_conn = DatabaseConnection(self.database_path)

				# Generate the query
				query_text = 'SELECT * FROM list WHERE user_id = ' + str(user_id) + ' AND listname = "' + listname + '"'

				list_row = db_conn.query(query_text).fetchone()

				return self.get_dictionary_from_list_record(list_row)

			else:
				print('ERROR: List does not exist')

		else:
			print('ERROR: User does not exist')

	# Get all the translations (words) of a list
	def get_translations_for_list(self, username, listname):

		list_id = self.get_list(username, listname).get("id")
		db_conn = DatabaseConnection(self.database_path)

		query_text = 'SELECT * FROM translation WHERE list_id = ' + str(list_id)

		translation_rows = db_conn.query(query_text).fetchall()

		# Map the results of dictionary_from_translation on translation_dictionaries
		translation_dictionaries = list(map(self.get_dictionary_from_translation_record, translation_rows))
		return translation_dictionaries

	# Generate a Python dictionary from a user record
	def get_dictionary_from_user_record(self, user_record):
		return {
			"id": user_record[0],
			"username": user_record[1],
			"email": user_record[2],
			"email_verified": user_record[3],
			"password_hash": user_record[4],
		}

	# Generate a Python dictionary from a list record
	def get_dictionary_from_list_record(self, list_record):
		return {
			"id": list_record[0],
			"user_id": list_record[1],
			"listname": list_record[2],
			"language_1_tag": list_record[3],
			"language_2_tag": list_record[4],
			"shared_with": str(list_record[5])
		}

	# Generate a Python dictionary from a translation record
	def get_dictionary_from_translation_record(self, translation_record):
		return {
			"id": translation_record[0],
			"list_id": translation_record[1],
			"language_1_text": translation_record[2],
			"language_2_text": translation_record[3]
		}
