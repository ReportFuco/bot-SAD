from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from app.schemas.news import NoticiaCreate, NoticiaResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models.news import Noticia


router = APIRouter(prefix="/news", tags=["News"])

@router.get("/", response_model=list[NoticiaResponse])
async def obtener_noticias(db: AsyncSession = Depends(get_db)):
    stmt = select(Noticia).options(selectinload(Noticia.dominio))
    result = await db.execute(stmt)
    noticias = result.scalars().all()
    return noticias


@router.get("/{noticia_id}", response_model=NoticiaResponse)
async def obtener_noticia_id(noticia_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Noticia).options(selectinload(Noticia.dominio)).where(Noticia.id_noticia == noticia_id)
    result = await db.execute(stmt)
    noticia = result.scalar_one_or_none()
    if noticia:
        return noticia
    raise HTTPException(status_code=404, detail="Noticia no encontrada")


@router.post("/create", response_model=NoticiaResponse)
async def crear_noticia(noticia: NoticiaCreate, session: AsyncSession = Depends(get_db)):

    existing = await session.execute(
        select(Noticia).where(Noticia.url_noticia == noticia.url_noticia)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail=f"La noticia con URL '{noticia.url_noticia}' ya existe."
        )

    nueva_noticia = Noticia(**noticia.model_dump())
    session.add(nueva_noticia)
    await session.commit()

    result = await session.execute(
        select(Noticia)
        .options(selectinload(Noticia.dominio))
        .where(Noticia.id_noticia == nueva_noticia.id_noticia)
    )
    noticia_con_dominio = result.scalar_one()

    return noticia_con_dominio


@router.delete("/{noticia_id}")
async def eliminar_noticia(noticia_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Noticia).where(Noticia.id_noticia == noticia_id)
    result = await db.execute(stmt)
    noticia = result.scalar_one_or_none()
    if noticia:
        await db.delete(noticia)
        await db.commit()
        return {"message": "Noticia eliminada"}
    return HTTPException(status_code=404, detail="Noticia no encontrada")
