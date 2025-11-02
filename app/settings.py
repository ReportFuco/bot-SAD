from dotenv import load_dotenv
import os


load_dotenv()

# Crendenciales de WordPress Ej: user,password
CREDENCIALS: tuple[str, ...] = tuple((os.getenv("USER_SAD") or "").split(","))

# URL de la web API de WordPress.
URL_SAD = os.getenv("URL_SAD") or ""

# Token de OpenAI para manipular Chatgpt entre otros modelos.
API_KEY_OPENAI = os.getenv("TOKEN_OPENAI")

# Credenciales de Evolution API
EVOLUTION_CREDENCIALS: dict[str, str] = {
    "url": os.getenv("URL_EVOLUTION") or "",
    "instance": os.getenv("INSTANCE_EVOLUTION") or "",
    "api_key": os.getenv("API_KEY_EVOLUTION") or ""
}

API_KEY_NEWSAPI = os.getenv("API_KEY_NEWSAPI") or ""
