from fastapi import FastAPI, HTTPException, status, Depends
from model import Carro
from typing import Optional, Any

app = FastAPI(title="API de Carros", version="1.0", description="Gerenciamento de Carros")

# Banco de dados fake
carros_db = {
    1: {
        "marca": "Toyota",
        "modelo": "Corolla",
        "ano": 2020,
        "preco": 90000.0,
        "imagem": "https://th.bing.com/th/id/OIP.ITVBnVyq-_NODNJSWxwJdQHaEK?rs=1&pid=ImgDetMain"
    },
    2: {
        "marca": "Honda",
        "modelo": "Civic",
        "ano": 2019,
        "preco": 85000.0,
        "imagem": "https://th.bing.com/th/id/OIP.t27LAgENBV78nDMgJcjIiAHaE8?rs=1&pid=ImgDetMain"
    },
    3: {
        "marca": "Ford",
        "modelo": "Focus",
        "ano": 2021,
        "preco": 95000.0,
        "imagem": "https://th.bing.com/th/id/R.bcf849ba929c1754c7fecf04a6854ae5?rik=RQB%2fLUqfGCA%2bOA&pid=ImgRaw&r=0"
    }
}

def fake_db():
    try:
        print("Conectando ao banco de dados...")
    finally:
        print("Fechando a conexão ao banco de dados.")

@app.get("/", description="Endpoint inicial")
async def home():
    return {"mensagem": "Bem-vindo à API de Carros"}

@app.get("/carros", description="Retorna todos os carros", summary="Obter lista de carros")
async def get_carros(db: Any = Depends(fake_db)):
    return carros_db

@app.get("/carros/{carro_id}", description="Retorna um carro pelo ID")
async def get_carro(carro_id: int):
    try:
        carro = carros_db[carro_id]
        return carro
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado")

@app.post("/carros", status_code=status.HTTP_201_CREATED, description="Adiciona um novo carro")
async def post_carro(carro: Carro):
    next_id = len(carros_db) + 1
    carros_db[next_id] = carro.dict()
    carros_db[next_id].pop("id", None) 
    return carros_db[next_id]

@app.put("/carros/{carro_id}", status_code=status.HTTP_202_ACCEPTED, description="Atualiza os dados de um carro existente")
async def put_carro(carro_id: int, carro: Carro):
    if carro_id in carros_db:
        carros_db[carro_id] = carro.dict()
        carros_db[carro_id].pop("id", None)
        return carros_db[carro_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe carro com o ID {carro_id}")

@app.delete("/carros/{carro_id}", status_code=status.HTTP_204_NO_CONTENT, description="Exclui um carro pelo ID")
async def delete_carro(carro_id: int):
    if carro_id in carros_db:
        del carros_db[carro_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe carro com o ID {carro_id}")

# Código para rodar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
