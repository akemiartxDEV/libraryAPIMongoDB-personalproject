from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI(
    title="API Biblioteca",
    description="API de estudo para registrar livros, usuários e empréstimos de uma biblioteca.",
    version="0.1.0",
)

cliente = MongoClient("mongodb://localhost:27017")
banco = cliente["biblioteca"]
livros = banco["livros"]


@app.get("/")
def raiz():
    return {"mensagem": "API da biblioteca funcionando"}


@app.get("/livros")
def listar_livros():
    lista = []
    for livro in livros.find():
        livro["_id"] = str(livro["_id"])
        lista.append(livro)
    return lista