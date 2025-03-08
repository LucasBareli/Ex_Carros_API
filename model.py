from typing import Optional
from pydantic import BaseModel

# Modelo para os carros
class Carro(BaseModel):
    id: Optional[int] = None
    marca: str
    modelo: str
    ano: int
    preco: float
    imagem: str