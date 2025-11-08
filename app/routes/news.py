from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from app.schemas.news import NoticiaCreate, NoticiaResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models.news import Noticia


router = APIRouter(prefix="/news", tags=["News"])

@router.get("/", response_model=list[NoticiaResponse])
async def leer_noticias(db: AsyncSession = Depends(get_db)):
    stmt = select(Noticia).options(selectinload(Noticia.dominio))
    result = await db.execute(stmt)
    noticias = result.scalars().all()
    return noticias

@router.post("/noticias", response_model=NoticiaResponse)
async def create_noticia(noticia: NoticiaCreate, session: AsyncSession = Depends(get_db)):

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


