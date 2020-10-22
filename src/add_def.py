"""
Read the vocabulary JSON file and update it with definitions
"""
import requests
import json

# Fetch credentials
with open('data/credentials.json', 'r') as f:
    cred = json.load(f)

# Default language
language = "en-gb"


def fetch_definition(word):
    """
    Contact the Oxford Dictionary API and fetch a definition
    TODO: could be improved if passed a list of word?
    """
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + \
        language + "/" + word.lower()
    result = requests.get(url, headers=cred).json()

    # Check if the API has returned an error
    try:
        result['error']
        return ''
    except KeyError:
        # TODO: look into the documentation of Oxford API to understand the
        # json structure
        # TODO: for now only the first definition is fetched, but it is a
        # possibility that there are others, so it should be accounted for
        # in a future update
        return result["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]


# Read the words for which we will fetch the definition
with open('data/vocab.json', 'r') as f:
    vocab = json.load(f)


# Populate the definitions list
definitions = []
for word in vocab["stems"]:
    definitions.append(fetch_definition(word))
vocab["definitions"] = definitions

# Write to disk
with open('data/vocab.json', 'w') as f:
    json.dump(vocab, f, indent=4)
