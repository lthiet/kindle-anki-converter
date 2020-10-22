import sqlite3
import json
"""
This script convert the vocabulary database then export it as
JSON for easier querying and processing. The fields we are interested
in is the stem and usage. The definition has to be fetched from
an API.
Author: Lam
"""

# Create a connection with vocabulary db
conn = sqlite3.connect('../data/vocab.db')
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

# Write to DISK
with open('../data/vocab.json', 'w') as f:
    json.dump(export, f, indent=4)
