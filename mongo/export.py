import ijson
from pymongo import MongoClient

def import_large_json(json_file_path, database_name, collection_name):
    """Processa JSONs muito grandes usando streaming"""
    client = MongoClient("mongodb+srv://thiagopls1:CEzSRhFpkJnMK4yL@cluster-teste.wjaszlz.mongodb.net/")
    collection = client[database_name][collection_name]
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        # Processa o JSON em streaming (item por item)
        objects = ijson.items(file, 'item')
        
        batch = []
        batch_size = 100
        
        for obj in objects:
            batch.append(obj)
            
            if len(batch) >= batch_size:
                collection.insert_many(batch)
                batch = []
                print(f"Inserido lote de {batch_size} documentos")
        
        # Inserir documentos restantes
        if batch:
            collection.insert_many(batch)
    
    client.close()

if __name__ == "__main__":
    db_name = "pokedb"
    import_large_json("./output/abilities.json", db_name, "abilities")
    import_large_json("./output/pokemons.json", db_name, "pokemons")
