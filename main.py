import argparse
import yaml
import sqlite3
import pandas
import traceback
import requests

# Global parameters
# TODO: put this in a config file instead
language = "en-gb"


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--appid",
                        help='Application ID from the Dictionnary')
    parser.add_argument("--key",
                        help='Application key from the Dictionnary')
    parser.add_argument("--vocab", required=True,
                        help='The absolute path to your vocab.db file')
    parser.add_argument("--clear", action='store_true',
                        help='Whether or not vocab.db should be cleared at the end')
    result = parser.parse_args()
    return vars(result)


def read_vocab(path):
    """
    Read the vocab.db file
    """
    # Create a connection with vocabulary db
    conn = sqlite3.connect(path)
    c = conn.cursor()

    # Select appropriate data
    c.execute("""
    SELECT words.stem, lookups.usage
        FROM words
        JOIN lookups
        ON words.id = lookups.word_key
    """)

    # Export to JSON
    export = {"stems": [], "usages": []}
    db = c.fetchall()
    for row in db:
        export["stems"].append(row[0])
        export["usages"].append(row[1])

    return export


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
        res = input(f"Definition not found for ->{word}<-, input your own:\n")
        return res
    except KeyError:
        # TODO: look into the documentation of Oxford API to understand the
        # json structure
        # TODO: for now only the first definition is fetched, but it is a
        # possibility that there are others, so it should be accounted for
        # in a future update
        return result["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]


if __name__ == "__main__":
    # Parse the arguments
    args = get_args()

    # Check if the user provided API key
    cred = None
    if args['appid'] == None or args['key'] == None:
        # The user didn't provide API key, try to read from cred.yaml
        try:
            with open('data/cred.yaml', 'r') as f:
                cred = yaml.safe_load(f)
        except:
            traceback.print_exc()
    else:
        # The user provided API key, write it inside a file for future use
        cred = {
            "app_id": args['appid'],
            "app_key": args['key']
        }
        with open('data/cred.yaml', 'w') as f:
            f.write(yaml.safe_dump(cred))

    # Read the vocab database
    vocab = read_vocab(args['vocab'])

    # Populate the definitions list
    definitions = []
    for word in vocab["stems"]:
        definitions.append(fetch_definition(word))

    vocab["definitions"] = definitions

    # Write to disk the anki deck
    pandas.DataFrame.from_dict(vocab).to_csv('data/vocab.csv')
