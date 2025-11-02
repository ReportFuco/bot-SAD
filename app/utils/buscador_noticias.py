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
        dia_anterior = (hoy - timedelta(days=4))

        params:dict[str, str | int] = {
            "q": 'supermercados OR retail AND chile',
            "language": "es",
            "sortBy": "relevancy",
            "from": dia_anterior.strftime("%Y-%m-%d"),
            "to": hoy.strftime("%Y-%m-%d"),
            "pageSize":20,
            "apiKey": self.api_key
        }

        res = httpx.get(self.BASE_URL, params=params) 
        data = res.json()

        if res.status_code == 200:
            bot.enviar_mensaje(
                numero=numero,
                mensaje=f"Claro, he encontrado {len(data['articles'])} noticias desde {dia_anterior.strftime('%d-%m-%Y')} hasta {hoy.strftime('%d-%m-%Y')}!"
            )
            for article in data["articles"]:

                bot.enviar_mensaje(
                    numero=numero,
                    mensaje=f"""
Titulo: {article["title"]}
                    
Fecha: {datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d-%m-%Y')}
                    
Contenido: {article["content"]}
                    
URL: {article["url"]}""")
        else:

            bot.enviar_mensaje(
                numero=numero, 
                mensaje=f"hubo un problema al obtener imagenes {res.status_code} - {res.text}"
            )

