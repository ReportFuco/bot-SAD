from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.news import Usuario, Noticia, Dominio
from app.schemas.news import NoticiaBase


async def obtener_info_numero(db: AsyncSession, numero_telefono: str):
    stmt = select(Usuario).where(Usuario.numero_telefono == numero_telefono)
    result = await db.execute(stmt)
    usuario = result.scalar_one_or_none()
    return usuario


async def guardar_noticia(session: AsyncSession, data: NoticiaBase, dominio_nombre: str):
    """Guarda una noticia y crea el dominio si no existe."""

    # 1. Buscar dominio existente
    result = await session.execute(
        select(Dominio).where(Dominio.nombre_dominio == dominio_nombre)
    )
    dominio = result.scalar_one_or_none()

    if dominio is None:
        dominio = Dominio(nombre_dominio=dominio_nombre)
        session.add(dominio)
        await session.flush()

    existe = await session.execute(
        select(Noticia).where(Noticia.url_noticia == data.url_noticia)
    )
    if existe.scalar_one_or_none():
        return None

    # 4. Crear la noticia
    noticia = Noticia(
        titulo=data.titulo,
        descripcion=data.descripcion,
        url_noticia=data.url_noticia,
        url_imagen=data.url_imagen,
        autor=data.autor,
        fecha_publicacion=data.fecha_publicacion,
        contenido=data.contenido,
        id_dominio=dominio.id_dominio,
    )

    session.add(noticia)
    await session.commit()
    await session.refresh(noticia)

    return noticia