import json
from bson.objectid import ObjectId
from pymongo import MongoClient


client = MongoClient("mongodb://localhost")
db = client.hw10

with open('utils/quotes.json', 'r', encoding='utf-8') as fd:
    data = json.load(fd)
    for el in data:
        author = db.authors.find_one({'fullname': el['author']})
        if author:
            db.quotes.insert_one({'quote': el['quote'],
                                  'tags':  el['tags'],
                                  'author': ObjectId(author['_id'])})
