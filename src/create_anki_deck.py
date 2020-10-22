"""
Read the JSON and create the Anki Deck
"""
import json
import csv
import pandas

# This assumes add_def.py was ran before
df = pandas.read_json('../data/vocab.json')

# Write to disk
df.to_csv(r'../data/vocab.csv')
