import httpx
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from app.utils.whatsapp import BotWhatsApp


class BuscadorNoticias:

    BASE_URL = "https://newsapi.org/v2/everything"
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_news(self, bot:BotWhatsApp, numero:str):
        
        hoy = datetime.now(ZoneInfo("America/Santiago"))
        dia_anterior = (hoy - timedelta(days=4)).strftime("%Y-%m-%d")

        params:dict[str, str] = {
            "q": "retail supermercados",
            "language": "es",
            "sortBy": "publishedAt",
            "from": dia_anterior,
            "to": hoy.strftime("%Y-%m-%d"),
            "apiKey": self.api_key
        }

        res = httpx.get(self.BASE_URL, params=params)
        data = res.json()

        if res.status_code == 200:
            for article in data["articles"]:

                bot.enviar_mensaje(
                    numero=numero,
                    mensaje=f"""Titulo: {article['title']}\n{article['content']}\n\n{article['url']}""",
                    )
        else:

            bot.enviar_mensaje(
                numero=numero, 
                mensaje=f"hubo un problema al obtener imagenes {res.status_code} - {res.text}"
            )

