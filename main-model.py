from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

def clasificar_opinion(texto: str) -> str:
    # Aquí iría el código de tu modelo de clasificación
    # En este caso, devolverá "OK" o "BAD" de manera aleatoria
    import random
    return random.choice(["OK", "BAD"])

class Opinion(BaseModel):
    texto: str

# Instanciar nuestra API
app = FastAPI()



@app.post("/opinions")
async def clasificar_opinion_random(opinion: Opinion):
    resultado = clasificar_opinion(opinion.texto)
    return {"resultado": resultado}
