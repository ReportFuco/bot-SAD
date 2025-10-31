from dotenv import load_dotenv
import os



load_dotenv()
CREDENCIALS: tuple[str, ...] = tuple((os.getenv("USER_SAD") or "").split(","))

URL_SAD = os.getenv("URL_SAD") or ""
