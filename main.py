import argparse
import yaml
import sqlite3
import pandas
import traceback
import requests

# Global parameters
# TODO: put this in a config file instead
language = "en-gb"


def get_config():
    # Check if this is a first run or not
    first_run = True
    try:
        with open('data/config.yaml') as f:
            first_run = False
    except:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--app_id", required=first_run,
                        help='Application ID from the Dictionnary')
    parser.add_argument("--app_key", required=first_run,
                        help='Application key from the Dictionnary')
    parser.add_argument("--vocab", required=first_run,
                        help='The absolute path to your vocab.db file')
    parser.add_argument("--clear", action='store_true',
                        help='Whether or not vocab.db should be cleared at the end')
    parser.add_argument("--lang", default="en-us")
    config = vars(parser.parse_args())

    if not first_run:
        with open('data/config.yaml', 'r') as f:
            config_disk = yaml.safe_load(f)

        # Update config
        for k in config_disk:
            if config[k] != None:  # TODO: check if value isn't equal to default
                config_disk[k] = config[k]

        config = config_disk

    with open('data/config.yaml', 'w') as f:
        f.write(yaml.safe_dump(config))

    return config


def read_vocab(path, n=None):
    """
    Read the vocab.db file
    n : maximum number of files to read
    """
    # Create a connection with vocabulary db
    conn = sqlite3.connect(path)
    c = conn.cursor()

    # Select appropriate data
    c.execute(f"""
    SELECT words.stem, lookups.usage
        FROM words
        JOIN lookups
        ON words.id = lookups.word_key
        ORDER BY words.stem
        {
            "" if n == None
            else f"LIMIT {n} "
        }
    """)

    # Export to JSON
    export = {"stems": [], "usages": []}
    db = c.fetchall()
    for row in db:
        export["stems"].append(row[0])
        export["usages"].append(row[1])

    return export


def fetch_definition(word, cred):
    """
    Contact the Oxford Dictionary API and fetch a definition
    TODO: could be improved if passed a list of word?
    """
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + \
        language + "/" + word.lower()
    result = requests.get(url, headers=cred)

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


def split_vocab(vocab):
    print(vocab)


if __name__ == "__main__":
    # Parse the config
    cfg = get_config()

    # Read the vocab database
    vocab = read_vocab(cfg['vocab'])

    # Split the vocab and write them to disk for future processing
    split_vocab(vocab)
    exit(0)

    # Populate the definitions list
    definitions = []
    for word in vocab["stems"]:
        cred = {
            "app_id": cfg["app_id"],
            "app_key": cfg["app_key"]
        }
        definitions.append(fetch_definition(word, cred))

    vocab["definitions"] = definitions

    # Write to disk the anki deck
    pandas.DataFrame.from_dict(vocab).to_csv('data/vocab.csv')
