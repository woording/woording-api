import sqlite3

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

	def get_user_list():
		db_conn = DatabaseConnection(database_path)

	def create_user(self, username, email, email_verified, password_hash):

		# Check if the username is available
		if not self.username_exists(username):
			# TODO: MAKE THIS MORE SECURE!
			# This method is really insecure and allows for SQL Injection

			# Create a DatabaseConnection
			db_conn = DatabaseConnection(self.database_path)

			# Genereate the query
			query_text = 'INSERT INTO user (username, email, email_verified, password_hash) VALUES ("' + username + '", "' + email + '", "' + str(int(email_verified)) + '", "' + password_hash + '")'

			# Use the query to create a new user
			db_conn.query(query_text)

		else:
			# TODO Handle username is not available error
			print ('ERROR: Username is not available')


	def get_user_info(self, username_to_check): 

		# Check if the user exists
		if self.username_exists(username_to_check):

			# Create a DatabaseConnection
			db_conn = DatabaseConnection(self.database_path)

			# Generate the query
			query_text = 'SELECT * FROM user WHERE username = "' + username_to_check + '"'

			user_info = db_conn.query(query_text).fetchone()


			return {
				"username": user_info[1],
				"email": user_info[2],
				"email_verified": user_info[3],
				"password_hash": user_info[4]
			}

		else:
			print ('ERROR: User does not exist')



	def username_exists(self, username_to_check):

		# If the username is not in the username list, it is not available
		return username_to_check in self.get_username_list()


	def get_username_list(self):
		
		# Create a DatabaseConnection
		db_conn = DatabaseConnection(self.database_path)

		# Get all the username rows
		username_rows = db_conn.query('SELECT username FROM user').fetchall()

		# Extract the first item
		usernames = tuple(username[0] for username in username_rows)
		
		return usernames

