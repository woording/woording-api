from database import *

db_manager = DatabaseManager()

# Create users
db_manager.create_user('cor', 'cor@pruijs.nl', True, 'Hunter2')
db_manager.create_user('leon', 'leon@grasmeijer.nl', False, 'Hunter23')
db_manager.create_user('philip', 'philip@debruijn.nl', False, 'Hunter23')

# Trying to create a user with a username that is taken returns an error
db_manager.create_user('cor', 'cor@pruijs.nl', False, 'Hunter2')


# Get a list of all usernames
print(db_manager.get_username_list())

# Check if a username exists
print(db_manager.username_exists('cor'))  # True
print(db_manager.username_exists('henk')) # False


# Get user info by name
print(db_manager.get_user_info('cor'))
print(db_manager.get_user_info('leon'))
print(db_manager.get_user_info('philip'))

# Trying to get user info of a user that doesn't exist returns an error
db_manager.get_user_info('henk')

