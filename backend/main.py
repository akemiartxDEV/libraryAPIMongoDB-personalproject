from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from bson.errors import InvalidId

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

class LivroNovo(BaseModel):
    titulo: str
    autor: str
    ano: int
    exemplares: int = 1


@app.post("/livros", status_code=201)
def cadastrar_livro(livro: LivroNovo):
    documento = livro.model_dump()
    documento["disponivel"] = documento["exemplares"] > 0
    resultado = livros.insert_one(documento)
    return {"mensagem": "Livro cadastrado com sucesso", "id": str(resultado.inserted_id)}

@app.get("/livros/{livro_id}")
def buscar_livro(livro_id: str):
    try:
        objeto_id = ObjectId(livro_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    livro = livros.find_one({"_id": objeto_id})
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    livro["_id"] = str(livro["_id"])
    return livro