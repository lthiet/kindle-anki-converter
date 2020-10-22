import requests
import json
import sys

# with open('../data/credentials.json', 'r') as f:
#     cred = json.load(f)

# language = "en-gb"
# word_id = "superfluous"
# url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + \
#     language + "/" + word_id.lower()
# r = requests.get(url, headers=cred)

# with open('../data/test.json', 'w') as f:
#     json.dump(r.json(), f, indent=4)

with open('../data/test.json', 'r') as f:
    data = json.load(f)


def fetch_definition(entry):
    # TODO: look into the documentation of Oxford API to understand the
    # json structure
    return entry["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"]
