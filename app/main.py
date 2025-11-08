from fastapi import FastAPI
from app.routes import webhook, news, domains
from app.settings import PORT, PROTOCOL, URL_SERVER


app = FastAPI(
    title="API de Automatización Supermercados al Día", 
    version="1.0.0", 
    description="""
        API para la automatización de tareas utilizando diversas integraciones como WordPress, OpenAI, Evolution API, y NewsAPI."""
    )

# Incluir las rutas del webhook
app.include_router(webhook.router)
app.include_router(news.router)
app.include_router(domains.router)

# Ruta raíz para verificar que la API está funcionando
@app.get("/")
def root()-> dict[str, str | int]:
    return {
        "INFO": f"Bienvenido a la API de Automatizazcion, para obtener información visite {URL_SERVER}/docs",
        "PORT": PORT,
        "PROTOCOL": PROTOCOL
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=PORT, 
        reload=True
    )