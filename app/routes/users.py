from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.news import Usuario, UsuarioNoticia, Noticia
from app.schemas.users import UserCreate
from typing import Any
from app.db import get_db
from sqlalchemy import select
from typing import Any


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def obtener_usuarios(db: AsyncSession = Depends(get_db))->list[dict[str, Any]]:
    result = await db.execute(select(Usuario))
    users = result.scalars().all()
    return [{
        "id": d.id_usuario,
        "numero": d.numero_telefono,
        "nombre": d.nombre,
        "creado": d.created_at.strftime("%d-%m-%Y")
        } for d in users]

@router.get("/{user_id}")
async def obtener_usuario_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id_usuario == user_id))
    user = result.scalar_one_or_none()
    if user:
        return user
    return HTTPException(status_code=404, detail="Usuario no encontrado")

@router.get("/{user_id}/noticias-vistas")
async def obtener_vistas_por_usuario(
    user_id:int, 
    db:AsyncSession = Depends(get_db),
    limit_vistas: int = 50
)-> dict[str, Any]:
    
    result_usuario = await db.execute(
        select(Usuario).where(Usuario.id_usuario == user_id)
    )

    usuario = result_usuario.scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=404, 
            detail="Usuario no encontrado")

    result_usuario_noticia = await db.execute(
        select(UsuarioNoticia).where(
            UsuarioNoticia.id_usuario == usuario.id_usuario
        ).limit(min(limit_vistas, 50)))
    
    usuario_noticia = result_usuario_noticia.scalars().all()

    return {
        "usuario": usuario.nombre,
        "numero": usuario.numero_telefono,
        "vistas": [{
            "id":un.id_usuario_noticia,
            "id_noticia": un.id_noticia,
            "fecha_vista":un.fecha_vista.strftime("%d-%m-%Y")
            } for un in usuario_noticia],
        "total_vistas": len(usuario_noticia)
    }

@router.get("/{user_id}/noticias-no-vistas")
async def obtener_noticias_no_vistas(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    limit_vistas: int = 50
)-> dict[str, Any]:

    subq = (
        select(UsuarioNoticia.id_noticia)
        .where(UsuarioNoticia.id_usuario == user_id)
    ).subquery()

    result = await db.execute(
        select(Noticia)
        .where(Noticia.id_noticia.not_in(select(subq.c.id_noticia)))
        .limit(min(limit_vistas, 50))
    )

    noticias = result.scalars().all()

    return {
        "noticias_no_vistas": [{
            "id_noticia": n.id_noticia,
            "titulo": n.titulo,
            "descripcion":n.descripcion,
            "url_noticia": n.url_noticia,
            "url_imagen": n.url_imagen,
            "fecha_publicacion": n.fecha_publicacion.strftime("%d-%m-%Y"),
            "contenido": n.contenido
            } for n in noticias],
        "total_no_vistas": len(noticias)    
    }

@router.post("/create")
async def crear_usuario(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(Usuario).where(Usuario.numero_telefono == user.numero_telefono)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"El usuario con número de teléfono '{user.numero_telefono}' ya existe."
        )

    nuevo_usuario = Usuario(
        numero_telefono=user.numero_telefono.title(),
        nombre=user.nombre,
        permiso=user.permiso
    )
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario