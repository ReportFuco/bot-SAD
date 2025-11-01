from fastapi import FastAPI
from app.routes import webhook


app = FastAPI()

app.include_router(webhook.router)

@app.get("/")
def root():
    return {"Bienvenida": "Bienvenido a la API de Automatizazcion"}