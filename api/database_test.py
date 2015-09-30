from database import *
from passlib.hash import sha512_crypt

SECURITY_PASSWORD_SALT = 'securitykey'

db_manager = DatabaseManager()

# Create users
db_manager.create_user('cor', 'cor@pruijs.nl', True, sha512_crypt.encrypt('Hunter2', salt=SECURITY_PASSWORD_SALT, rounds=5000))
db_manager.create_user('leon', 'leon@grasmeijer.nl', True, sha512_crypt.encrypt('all_i_see_is_*****', salt=SECURITY_PASSWORD_SALT, rounds=5000))
db_manager.create_user('philip', 'philip@debruijn.nl', True, sha512_crypt.encrypt('***hunter***', salt=SECURITY_PASSWORD_SALT, rounds=5000))

# Create lists
db_manager.create_list('cor', 'duitse_woorden', 'dut', 'ger', '2')
db_manager.create_list('cor', 'engelse_woorden', 'dut', 'eng', '1')

db_manager.create_list('leon', 'latijn_woorden', 'dut', 'lat', '0')

# Create translations
db_manager.create_translation('cor', 'engelse_woorden', 'auto', 'car')
db_manager.create_translation('cor', 'engelse_woorden', 'boom', 'tree')
db_manager.create_translation('cor', 'engelse_woorden', 'moeder', 'mother')
db_manager.create_translation('cor', 'engelse_woorden', 'vader', 'father')
db_manager.create_translation('cor', 'engelse_woorden', 'broer', 'bro')
db_manager.create_translation('cor', 'engelse_woorden', 'muis', 'mouse')
db_manager.create_translation('cor', 'engelse_woorden', 'toetsenbord', 'keyboard')
db_manager.create_translation('cor', 'engelse_woorden', 'fiets', 'bike')
db_manager.create_translation('cor', 'engelse_woorden', 'appel', 'apple')
db_manager.create_translation('cor', 'engelse_woorden', 'ding', 'thing')
db_manager.create_translation('cor', 'engelse_woorden', 'wolk', 'cloud')
db_manager.create_translation('cor', 'engelse_woorden', 'scherm', 'screen')
db_manager.create_translation('cor', 'engelse_woorden', 'potlood', 'pencil')
db_manager.create_translation('cor', 'engelse_woorden', 'muziek', 'music')

db_manager.create_translation('cor', 'duitse_woorden', 'de auto', 'das Auto')
db_manager.create_translation('cor', 'duitse_woorden', 'kamp', 'kampf')
db_manager.create_translation('cor', 'duitse_woorden', 'geodriehoek', 'geometrie dreieck')

db_manager.create_translation('leon', 'latijn_woorden', 'rust', 'requiescat')
db_manager.create_translation('leon', 'latijn_woorden', 'in', 'im')
db_manager.create_translation('leon', 'latijn_woorden', 'vrede', 'pace')


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

print(db_manager.get_list('cor', 'engelse_woorden'))

print(db_manager.get_translations_for_list('cor', 'engelse_woorden'))




