import httpx
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Literal
import re
from datetime import datetime
from app.schemas.news import NoticiaBase

class BuscadorNoticias:

    BASE_URL = "https://newsapi.org/v2/everything"
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_news(
            self,
            sort_by:Literal["relevancy", "popularity", "publishedAt"] = "publishedAt",
            q:str = "supermercados OR retail"
            ) -> list[NoticiaBase]:
        
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

            return [
                NoticiaBase(
                    titulo = noticia["title"],
                    autor = noticia["author"] or "Desconocido",
                    descripcion = noticia["description"] or "Sin descripción",
                    url_noticia = noticia["url"],
                    url_imagen = noticia["urlToImage"] or "",
                    contenido = noticia["content"] or "",
                    dominio = busca_dominio.findall(
                        noticia['url'])[0] if busca_dominio.findall(noticia['url']) else None,
                    fecha_publicacion = datetime.strptime(
                        noticia['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'
                    )
                ) for noticia in retorno]

        else:
            raise RuntimeError(f"NewsAPI error {res.status_code}: {data}")
