import ijson
from pymongo import MongoClient
from decimal import Decimal
from bson.decimal128 import Decimal128

def convert_decimals_to_decimal128(obj):
    """
    Converte todos os valores Decimal para Decimal128 (suportado pelo MongoDB)
    """
    if isinstance(obj, Decimal):
        return Decimal128(str(obj))  # Converter para string primeiro
    elif isinstance(obj, dict):
        return {k: convert_decimals_to_decimal128(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals_to_decimal128(item) for item in obj]
    else:
        return obj

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
            new_obj = convert_decimals_to_decimal128(obj)
            batch.append(new_obj)
            
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
