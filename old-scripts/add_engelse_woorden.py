from database import *

db_manager = DatabaseManager()
db_manager.create_list('cor', 'engelse_woorden', 'dut', 'eng', '1')

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
