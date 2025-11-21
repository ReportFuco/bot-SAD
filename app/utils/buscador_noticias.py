import httpx
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Literal
import re


class BuscadorNoticias:

    BASE_URL = "https://newsapi.org/v2/everything"
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_news(
            self,
            sort_by:Literal["relevancy", "popularity", "publishedAt"] = "publishedAt",
            q:str = "supermercados OR retail"
            ) -> list[dict[str, str]] | dict[str, str] | None:
        
        hoy = datetime.now(ZoneInfo("America/Santiago"))
        dia_anterior = (hoy - timedelta(days=1))

        params:dict[str, str | int] = {
            "q": q,
            "language": "es",
            "sortBy": sort_by,
            "from": dia_anterior.strftime("%Y-%m-%d"),
            "to": hoy.strftime("%Y-%m-%d"),
            "pageSize":20,
            "apiKey": self.api_key
        }

        res = httpx.get(self.BASE_URL, params=params) 
        data = res.json()

        if res.status_code == 200:
            retorno = data.get("articles", [])
            busca_dominio = re.compile(
                r'\b([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)\b'
            )

            return [{
                "titulo": noticia["title"],
                "descripcion": noticia["description"] or "Sin descripción",
                "url_noticia": noticia["url"],
                "url_imagen": noticia["urlToImage"] or "",
                "autor": noticia["author"] or "Desconocido",
                "dominio": busca_dominio.findall(noticia['url'])[0] if busca_dominio.findall(noticia['url']) else "Desconocido",
                "fecha_publicacion": datetime.strptime(noticia['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d-%m-%Y')
            } for noticia in retorno]

        else:
            return {
                "error": f"No se pudieron obtener las noticias. Código de estado: {res.status_code}"
            }
