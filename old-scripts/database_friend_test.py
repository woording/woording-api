from database import *
from passlib.hash import sha512_crypt

SECURITY_PASSWORD_SALT = 'securitykey'

db_manager = DatabaseManager()

db_manager.create_friendship("cor", "leon")

print (db_manager.get_friends_for_user("cor"))