from pymongo import MongoClient
from pprint import pprint

def find_document_by_field(database_name, collection_name, field, value):
    client = MongoClient("mongodb+srv://thiagopls1:CEzSRhFpkJnMK4yL@cluster-teste.wjaszlz.mongodb.net/")
    collection = client[database_name][collection_name]
    return collection.find({field: value})    


if __name__ == '__main__':
    db_name = "pokedb"
    collection = "pokemons"
    result = find_document_by_field(db_name, collection, "id", 180)
    for document in result:
        pprint(document)

