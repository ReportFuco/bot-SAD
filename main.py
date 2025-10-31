import httpx
from pathlib import Path
from typing import Any
import settings

# -------------------------------
# 1️⃣ Subir imagen
# -------------------------------

path_imagen = Path("assets/image/images.webp")

headers = {
    "Content-Disposition": f'attachment; filename="{path_imagen.name}"',
    "Content-Type": "image/webp",
}

with path_imagen.open("rb") as img:
    response = httpx.post(settings.URL_SAD, headers=headers, auth=settings.CREDENCIALS, content=img)

if response.status_code == 201:
    data = response.json()
    print("✅ Imagen subida con éxito")
    print("🖼️ URL:", data["source_url"])
    print("🆔 ID:", data["id"])
    imagen_id = data["id"]
else:
    print("❌ Error al subir imagen")
    print(response.status_code, response.text)
    exit()

# -------------------------------
# 2️⃣ Crear post con esa imagen
# -------------------------------
post_url = f"https://supermercadosaldia.cl/wp-json/wp/v2/posts"

post_data: dict[str, str | Any] = {
    "title": "Nuevo producto destacado",
    "content": "Contenido del post generado por Python 🐍",
    "status": "publish",
    "featured_media": imagen_id,
}

response = httpx.post(post_url, auth=settings.CREDENCIALS, json=post_data)

if response.status_code == 201:
    post = response.json()
    print("✅ Post creado correctamente")
    print("🔗 Enlace:", post["link"])
else:
    print("❌ Error al crear el post")
    print(response.status_code, response.text)
