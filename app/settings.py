from dotenv import load_dotenv
import os


load_dotenv()

PORT: int = int(os.getenv("PORT") or 8000)
PROTOCOL: str = os.getenv("PROTOCOL") or "http"
URL_SERVER: str = os.getenv("URL_SERVER") or f"{PROTOCOL}://localhost:{PORT}"

# Crendenciales de WordPress Ej: user,password
CREDENCIALS: tuple[str, ...] = tuple((os.getenv("USER_SAD") or "").split(","))

# URL de la web API de WordPress.
URL_SAD:str = os.getenv("URL_SAD") or ""

# Token de OpenAI para manipular Chatgpt entre otros modelos.
API_KEY_OPENAI:str = os.getenv("TOKEN_OPENAI") or ""

# Credenciales de Evolution API
EVOLUTION_CREDENCIALS: dict[str, str] = {
    "url": os.getenv("URL_EVOLUTION") or "",
    "instance": os.getenv("INSTANCE_EVOLUTION") or "",
    "api_key": os.getenv("API_KEY_EVOLUTION") or ""
}

# API para conección con NewsAPI, encargado de buscar y encontrar las noticias
API_KEY_NEWSAPI:str = os.getenv("API_KEY_NEWSAPI") or ""

# Conección con la base de datos
DATABASE_URL:str = os.getenv("DATABASE_URL") or ""