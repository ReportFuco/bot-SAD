from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from app.schemas import NoticiaBase
from app.models import Usuario
from typing import Sequence
from app.models import (
    Usuario, Noticia, Dominio, UsuarioNoticia, MensajeProcesado
)


async def obtener_info_numero(db: AsyncSession, numero_telefono: str):

    stmt = select(Usuario).where(Usuario.numero_telefono == numero_telefono)
    result = await db.execute(stmt)
    usuario = result.scalar_one_or_none()
    return usuario

async def generar_vista_usuario(db:AsyncSession, usuario: Usuario)-> Sequence[Noticia] | None:

    if usuario:
        subq = (
            select(UsuarioNoticia.id_noticia)
            .where(
                UsuarioNoticia.id_usuario == usuario.id_usuario,
                UsuarioNoticia.id_noticia == Noticia.id_noticia
            )
        )

        result = await db.execute(
            select(Noticia)
            .where(~exists(subq))
        )
        noticias = result.scalars().all()
        if noticias:
            for n in noticias:
                db.add(UsuarioNoticia(
                    id_usuario=usuario.id_usuario,
                    id_noticia=n.id_noticia,
                    vista=True
                ))

            return noticias
        else:
            return None
    else: 
        return None

async def guardar_noticia(
        session: AsyncSession, 
        data: NoticiaBase, 
        dominio_nombre: str | None
    )-> Noticia | None:
    
    """Guarda una noticia y crea el dominio si no existe."""

    if dominio_nombre:

        result = await session.execute(
            select(Dominio).where(
                Dominio.nombre_dominio == dominio_nombre
            )
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

        dominio_final = dominio.id_dominio
    else:
        dominio_final = None

    noticia = Noticia(
        titulo=data.titulo,
        descripcion=data.descripcion,
        url_noticia=data.url_noticia,
        url_imagen=data.url_imagen,
        autor=data.autor,
        fecha_publicacion=data.fecha_publicacion,
        contenido=data.contenido,
        id_dominio=dominio_final,
    )

    session.add(noticia)
    await session.flush()

    return noticia


async def procesar_mensaje(
        db: AsyncSession, 
        message_id: str, 
        usuario: Usuario, 
        contenido_msg: str,
        tipo_mensaje:str
)-> bool:
    
    # 1. ¿Mensaje ya procesado?
    result = await db.execute(
        select(MensajeProcesado).where(
            MensajeProcesado.mensaje_id == message_id
        )
    )
    mensaje = result.scalar_one_or_none()

    if mensaje:
        return False

    # 3. Guardar nuevo registro
    nuevo_msg = MensajeProcesado(
        id_usuario=usuario.id_usuario,
        mensaje_id=message_id,
        contenido=contenido_msg,
        tipo_mensaje=tipo_mensaje
    )

    db.add(nuevo_msg)
    await db.flush()

    return True
