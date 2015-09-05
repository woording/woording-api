from database import *

#db_conn.query('INSERT INTO user (username, email, email_verified, password_hash) VALUES ("piet", "piet@email.com", "false", "pasword123")')

db_manager = DatabaseManager()

print db_manager.username_is_available('klaas') # true

print db_manager.username_is_available('piet') # false

