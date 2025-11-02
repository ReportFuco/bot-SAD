import httpx
from pathlib import Path
from typing import Any, Optional
from datetime import datetime


class WPConnect:
    """
    Clase para manipular el WordPress
    """
    def __init__(
            self, 
            url: str, 
            user: Optional[str] = None, 
            password:Optional[str] = None
        ) -> None:

        self.url = url
        self.auth:tuple[Optional[str], Optional[str]] = (user, password)

    def upload_img(
            self, 
            nombre_imagen: str, 
            path_imagen: Path
        ) -> tuple[Optional[str] , Optional[str]]:
        
        headers = {
            "Content-Disposition": f"attachment; filename="{nombre_imagen}"",
            "Content-Type": "image/jpeg",
        }

        with path_imagen.open("rb") as img:
            res = httpx.post(self.url, headers=headers, auth=self.auth, content=img)
        
        if res.status_code == 200:
            data = res.json()
            return data.get("source_url"), data.get("id")
        
        return None, None

    def get_news(self, per_page: int = 10) -> dict[str, Any]:
        """Obtiene los últimos posts publicados."""
        res = httpx.get(f"{self.url}/wp/v2/posts", params={"per_page": per_page})
        if res.status_code == 200:
            return res.json()
        return {"error": f"Problema al obtener información ({res.status_code})"}

    def get_news_id(self, id: int) -> dict[str, Any] | None:
        """Obtiene una noticia por ID"""
        res = httpx.get(f"{self.url}/wp/v2/posts/{id}")

        if res.status_code != 200:
            return None

        data = res.json()

        featured_links = data.get("_links", {}).get("wp:featuredmedia", [])
        foto = None
        if featured_links and isinstance(featured_links, list):
            res_foto_url = featured_links[0].get("href")
            if res_foto_url:
                res_foto = httpx.get(res_foto_url)
                if res_foto.status_code == 200:
                    foto_data = res_foto.json()
                    foto = foto_data.get("source_url")

        # 🔹 Transformar fecha ISO a datetime
        date_str = data.get("date")
        dt = None
        if date_str:
            try:
                dt = datetime.fromisoformat(date_str)
            except ValueError:
                pass

        return {
            "id": data.get("id"),
            "title": data.get("title", {}).get("rendered"),
            "content": data.get("content", {}).get("rendered"),
            "datetime": dt.strftime("%d/%m/%Y %H:%M") if dt else None,
            "image_link": foto,
        }

    def post_news(
            self, 
            title:str, 
            content:str, 
            status:str="publish", 
            id_img:str
        )-> dict[str, str | Any]:
        
        post_data:dict[str, str | Any] = {
            "title": title,
            "content": content,
            "status": status,
            "featured_media": id_img,
        }

        res = httpx.post(f"{self.url}/v2/posts", auth=self.auth, json=post_data)

        if res.status_code == 201:
            return res.json()
        else:
            return {"error": res.status_code, "mensaje": res.text}

