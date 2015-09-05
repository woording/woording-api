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

	def create_user(username, email, email_verified, password_hash):
		db_conn = DatabaseConnection(database_path)

	# Function that checks if username is available, returns a Boolean
	def username_is_available(self, username_to_check):
		# Create a DatabaseConnection
		db_conn = DatabaseConnection(self.database_path)

		# Get all the username rows
		username_rows = db_conn.query('SELECT username FROM user').fetchall()

		# Extract the first item
		usernames = tuple(username[0] for username in username_rows)

		# If the user name is in usernames, it is not available
		return not username_to_check in usernames

	def list_users(self):
		
		db_conn = DatabaseConnection(self.database_path)
		rows = db_conn.query('SELECT username FROM user').fetchall()
		
		return rows


