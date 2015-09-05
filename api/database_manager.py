import sqlite3

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
class DatabaseManager:
	def get_user_list():
		db_conn = DatabaseConnection('wording.db')


