import logging
import os
from pymongo import MongoClient
import json
from pymongo import DESCENDING

def init_db():
    DATA_DIR = os.environ['DB_DATA_DIR']
    DB_URL = os.environ['DB_URL']
    DB_NAME = os.environ['DB_NAME']
    DB_COLLECTION = os.environ['DB_COLLECTION']
    client = MongoClient(DB_URL)
    repo_db = client[DB_NAME]
    data_collection = repo_db[DB_COLLECTION]

    if DB_NAME not in client.list_database_names():
        files = os.listdir(DATA_DIR)
        print("Inserting repo data into MongoDB...")
        count = 0
        for file in files:
            if not file.endswith('.json'):
                continue
            with open(DATA_DIR + '/' + file, 'r') as f:
                try:
                    repo_data = json.load(f)
                except UnicodeDecodeError:
                    print("Encountered corrupted repo data, skip...")
                    continue
                data_collection.insert_many(repo_data)
            count += 1
            if count % 100_000 == 0:
                print(f'inserted {count} repos')
        print("Insertion complete")
    else:
        print('Encountered existing database, skip insertion step')

def get_last_page():
    DB_URL = os.environ['DB_URL']
    DB_NAME = os.environ['DB_NAME']
    DB_COLLECTION = os.environ['DB_COLLECTION']
    client = MongoClient(DB_URL)
    repo_db = client[DB_NAME]
    data_collection = repo_db[DB_COLLECTION]

    last_page = data_collection.find().sort('_id', -1)[0]

    if 'last_page' in dict(last_page).keys():
        return last_page
    else:
        return 1

def handle_page(page_json):
    DB_URL = os.environ['DB_URL']
    DB_NAME = os.environ['DB_NAME']
    DB_COLLECTION = os.environ['DB_COLLECTION']

    client = MongoClient(DB_URL)
    repo_db = client[DB_NAME]
    data_collection = repo_db[DB_COLLECTION]
    try:
        data_collection.insert_many(page_json)
        print('Page successifully written')
    except Exception as e:
        logging.error(e)
