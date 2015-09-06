import json

def createJsonList(name, language_one, language_two, words):
    jsonData = {
        'name': name,
        'languages': {
            'language-1': language_one,
            'language-2': language_two
            },
        'words': []
    }

    for i in xrange(0,len(words),2):
        jsonData['words'].append({language_one: words[i], language_two: words[i+1]})

    with open(name + '.json', 'w') as outfile:
        json.dump(jsonData, outfile)
