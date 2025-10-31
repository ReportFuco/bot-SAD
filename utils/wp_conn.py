import httpx
from pathlib import Path


class WPConnect:
    
    def __init__(self, url:str, user: str, password: str) -> None:
        self.url: str = url
        self.auth:tuple[str, str] = (user, password)


    def subir_imagen(self, nombre_imagen:str, path_imagen:Path)-> tuple[str | None, str | None]:
        headers = {
        "Content-Disposition": f'attachment; filename="{nombre_imagen}"',
        "Content-Type": "image/jpeg",
        }

        with path_imagen.open("rb") as img:
            res = httpx.post(self.url, headers=headers, auth=self.auth, content=img)
        
        if res.status_code == 200:
            data = res.json()
            return data["source_url"], data["id"]
        
        else:
            return None, None
