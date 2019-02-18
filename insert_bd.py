import json
from pymongo import MongoClient
import pymongo

client = MongoClient('mongodb://localhost:27017/') # conecta num cliente do MongoDB rodando na sua máquina
db = client['imdb'] # acessa o banco de dados
collection = db['movies_imdb_oficial'] # acessa a minha coleção dentro desse banco de dados
print("sucesso")

# Lendo o json e inserindo no banco
with open('mv.json') as f:
    file_data = json.load(f)
    collection.insert(file_data)
    client.close()
