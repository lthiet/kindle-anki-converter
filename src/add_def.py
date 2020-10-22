import requests
import json
import sys

with open('../data/credentials.json', 'r') as f:
    cred = json.load(f)

language = "en-gb"
word_id = "example"
url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + \
    language + "/" + word_id.lower()
r = requests.get(url, headers=cred)

print("code {}\n".format(r.status_code))
print("json \n" + json.dumps(r.json()))
