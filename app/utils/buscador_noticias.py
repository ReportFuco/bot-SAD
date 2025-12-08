import httpx
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Literal
from datetime import datetime
from app.schemas.news import NoticiaBase
from urllib.parse import urlparse

class BuscadorNoticias:

    BASE_URL = "https://newsapi.org/v2/everything"
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key


    @staticmethod
    def extraer_dominio(url: str) -> str:
        parsed = urlparse(url)
        host = parsed.netloc.lower()

        if host.startswith("www."):
            host = host[4:]

        partes = host.split('.')
        if len(partes) > 2:
            host = ".".join(partes[-2:])
        return host


    def get_news(
            self,
            sort_by:Literal["relevancy", "popularity", "publishedAt"] = "publishedAt",
            q:str = "supermercados OR retail"
            ) -> list[NoticiaBase]:
        
        hoy = datetime.now(ZoneInfo("America/Santiago"))
        dia_anterior = (hoy - timedelta(days=3))

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

            return [
                NoticiaBase(
                    titulo = noticia["title"],
                    autor = noticia["author"] or "Desconocido",
                    descripcion = noticia["description"] or "Sin descripción",
                    url_noticia = noticia["url"],
                    url_imagen = noticia["urlToImage"] or "",
                    contenido = noticia["content"] or "",
                    dominio = self.extraer_dominio(noticia['url']),
                    fecha_publicacion = datetime.strptime(
                        noticia['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'
                    )
                ) for noticia in retorno]

        else:
            raise RuntimeError(f"NewsAPI error {res.status_code}: {data}")
