from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.news import Noticia, UsuarioNoticia, PublicacionWordpress
from datetime import datetime
from typing import Any


async def marcar_como_vista(db: AsyncSession, id_usuario: int, id_noticia: int):
    stmt = select(UsuarioNoticia).where(
        UsuarioNoticia.id_usuario == id_usuario,
        UsuarioNoticia.id_noticia == id_noticia,
    )
    result = await db.execute(stmt)
    registro = result.scalar_one_or_none()

    if registro:
        registro.vista = True
    else:
        registro = UsuarioNoticia(id_usuario=id_usuario, id_noticia=id_noticia, vista=True)
        db.add(registro)

    await db.commit()
    return registro

async def registrar_publicacion_wp(db: AsyncSession, id_noticia: int, id_post_wp: int, url: str, publicado: bool):
    publicacion = PublicacionWordpress(
        id_noticia=id_noticia,
        id_post_wordpress=id_post_wp,
        url_publicacion=url,
        publicado=publicado,
        created_at=datetime.now()
    )
    db.add(publicacion)
    await db.commit()
    await db.refresh(publicacion)
    return publicacion


async def obtener_noticia_id(db: AsyncSession, id_noticia:int)->dict[str, Any] | None:
    busqueda = await db.execute(select(Noticia).where(
        Noticia.id_noticia == id_noticia
    ))

    noticia = busqueda.scalar_one_or_none()
    if noticia:
        return {
            "id": noticia.id_noticia,
            "titulo": noticia.titulo,
            "descripcion": noticia.descripcion,
            "URL": noticia.url_noticia,
            "imagen": noticia.url_imagen,
            "contenido": noticia.contenido,
            "fecha_publicacion": noticia.fecha_publicacion.strftime("%d-%m-%Y"),
        }
    else:
        return None