from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def root():
    return {"Bienvenida": "Bienvenido a la API de Automatizazcion"}