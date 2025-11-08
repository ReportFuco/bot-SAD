from fastapi import APIRouter, Depends
from app.schemas.news import NoticiaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.crud.news import upsert_noticia
from sqlalchemy import select
from app.models.news import Noticia


router = APIRouter(prefix="/news", tags=["News"])

@router.get("/")
async def leer_noticias(db: AsyncSession = Depends(get_db)):
    stmt = select(Noticia)
    result = await db.execute(stmt)
    noticias = result.scalars().all()
    return noticias

@router.post("/")
async def crear_noticia(
    noticia: NoticiaCreate,
    db: AsyncSession = Depends(get_db)
):
    return await upsert_noticia(db, noticia.model_dump())


