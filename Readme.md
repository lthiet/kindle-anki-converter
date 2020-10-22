# Kindle Anki Converter

This collection of script allow users to convert the **vocabulary builder dataset from Kindle** into
a **Anki back and reverse cards deck**. 

# Currently Supported Features

- the supported languages is English.
- The API used in this project is Oxford Dictionary.
- Only the fields of definitions is supported.

# Tutorial

## Requirements

You need to have `python` installed. Run this to install the requirements
```
$ pip install -r requirements.txt
```

## API credentials

The definitions aren't included in the dataset from Kindle. Therefore, queries to a 3rd party
that contains lexical definitions for words is Required. The supported API is the one from Oxford Dictionary. 

1. To get your credentials, visit this website : "https://developer.oxforddictionaries.com/"
2. Click on **Get Your API Key**
3. Choose your pricing based on personal preference.
4. Fill in the form to complete your registration.
5. Check your email for confirmation (could be in spam folder)
6. Once you are registered, visit the [website](https://developer.oxforddictionaries.com/) again
7. Click on **Credentials**
8. You should see a table with your business app name on the far left. Click on it.
9. Write down your **Application ID** and one of your **Application Keys** somewhere.

## Locating `vocab.db`

1. Plug your Kindle on your computer.
2. Look for the file named `vocab.db` inside the storage of your Kindle. By default on `Ubuntu 20.04`, it should look something like this : `/media/<user>/Kindle/system/vocabulary/vocab.db`
3. Make note of where it is located (have it in a opened file finder somewhere)

## Running the scripts

1. Make sure you are at the root of this repo.
2. Create a directory that will store the data and dumps of the scripts
```
$ mkdir data
```
3. Copy the `vocab.db` file inside the `data` directory. **If your `vocab.db` file is located at the default location**, you can use this command. Replace `<user>` with the name of your user folder
```
$ cp /media/<user>/Kindle/system/vocabulary/vocab.db data/
```
4. Run this script to let it know of your credentials. Replace the fields in brackets `<>` with the id and keys you obtained earlier.
```
$ python src/create_credentials.py <your_app_id> <your_app_key>
```
5. Run this script to extract the vocabulary from Kindle into another format with which it is easier to process
```
$ python src/read_db.py 
```
6. Run this script so that it queries the Oxford Dictionary. **This could take a while**
```
$ python src/add_def.py
```
7. Run this script to create a `csv` file which can be imported into Anki
```
$ python src/create_anki_deck.py
```

## Exporting to Anki

At this point, your file tree should look like this :
```
.
├── data
│   ├── credentials.json
│   ├── vocab.csv
│   ├── vocab.db
│   └── vocab.json
├── Readme.md
├── requirements.txt
└── src
    ├── add_def.py
    ├── create_anki_deck.py
    ├── create_credentials.py
    └── read_db.py
```

1. Open `vocab.csv` with Anki.
2. A window prompt should appear. Make sure that the card type and the field mapping should match as picture is shown. \
![You should have the same fields](doc/img/fields.png)
3. CLick **Import** and you should be done.
   
# Future Work

**TODO**