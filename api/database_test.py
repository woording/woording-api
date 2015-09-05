from database import *


db_manager = DatabaseManager()

# Create users
db_manager.create_user('cor', 'cor@pruijs.nl', True, 'Hunter2')
db_manager.create_user('leon', 'leon@grasmeijer.nl', False, 'Hunter23')
db_manager.create_user('philip', 'philip@debruijn.nl', False, 'Hunter23')

# Trying to create a user with a username that is taken returns an error
db_manager.create_user('cor', 'cor@pruijs.nl', False, 'Hunter2')



# Create lists
db_manager.create_list('cor', 'Duitse woorden', 'NL_nl', 'DE_de')
db_manager.create_list('cor', 'Engelse woorden', 'NL_nl', 'EN_en')

# Trying to create a list with an existing username/list combo returns an error
db_manager.create_list('cor', 'Engelse woorden', 'NL_nl', 'EN_en')
db_manager.create_translation('cor', 'Engelse woorden', 'auto', 'car')
db_manager.create_translation('cor', 'Engelse woorden', 'boom', 'tree')
db_manager.create_translation('cor', 'Engelse woorden', 'moeder', 'mother')


# Get a list of all usernames
print(db_manager.get_username_list())

# Check if a username exists
print(db_manager.username_exists('cor'))  # True
print(db_manager.username_exists('henk')) # False


# Get user info by name
print(db_manager.get_user('cor'))
print(db_manager.get_user('leon'))
print(db_manager.get_user('philip'))

# Trying to get user info of a user that doesn't exist returns an error
db_manager.get_user('henk')

# Get allt he lists for a user
print(db_manager.get_lists_for_user('cor'))

print(db_manager.get_list('cor', 'Engelse woorden'))

print(db_manager.get_translations_for_list('cor', 'Engelse woorden'))


