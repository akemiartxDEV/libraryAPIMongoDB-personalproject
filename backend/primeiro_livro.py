from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017")
banco = cliente["biblioteca"]
livros = banco["livros"]

livro = {
    "titulo": "Sharp Objects",
    "autor": "Gillian Flynn",
    "ano": 2010,
    "exemplares": 10,
    "disponivel": True
}

resultado = livros.insert_one(livro)
print("Livro guardado com id:", resultado.inserted_id)

for item in livros.find():
    print(item);