from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.news import Noticia, UsuarioNoticia, PublicacionWordpress
from datetime import datetime


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


async def get_noticias_no_vistas(db: AsyncSession, id_usuario: int, limit: int = 5):
    """
    Devuelve las noticias no vistas por el usuario.
    """
    subq = select(UsuarioNoticia.id_noticia).where(
        UsuarioNoticia.id_usuario == id_usuario,
        UsuarioNoticia.vista == True
    )

    stmt = (
        select(Noticia)
        .where(Noticia.id_noticia.not_in(subq))
        .order_by(Noticia.fecha_publicacion.desc())
        .limit(limit)
    )

    result = await db.execute(stmt)
    return result.scalars().all()


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
