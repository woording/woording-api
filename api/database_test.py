from database_manager import *

db_conn = DatabaseConnection('wording.db')
db_conn.query('INSERT INTO user (username, email, email_verified, password_hash) VALUES ("piet", "piet@email.com", "false", "pasword123")')